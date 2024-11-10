import datetime
from typing import cast
from flask import Blueprint, abort, jsonify, make_response, request
from spectree import Response
from models import Player, PlayerTeam, PlayerTeamAvailability, PlayerTeamRole, db
from middleware import requires_authentication
from spec import spec, BaseModel


api_schedule = Blueprint("schedule", __name__, url_prefix="/schedule")

class ViewScheduleForm(BaseModel):
    window_start: datetime.datetime
    team_id: int
    window_size_days: int = 7

class ViewScheduleResponse(BaseModel):
    availability: list[int]

@api_schedule.get("/")
@spec.validate(
    resp=Response(
        HTTP_200=ViewScheduleResponse
    )
)
@requires_authentication
def get(query: ViewScheduleForm, player: Player, **kwargs):
    window_start = query.window_start
    window_end = window_start + datetime.timedelta(days=query.window_size_days)

    availability_regions = db.session.query(
        PlayerTeamAvailability
    ).where(
        PlayerTeamAvailability.player_id == player.steam_id
    ).where(
        PlayerTeamAvailability.team_id == query.team_id
    ).where(
        PlayerTeamAvailability.start_time.between(window_start, window_end) |
        PlayerTeamAvailability.end_time.between(window_start, window_end) |

        # handle edge case where someone for some reason might list their
        # availability spanning more than a week total
        ((PlayerTeamAvailability.start_time < window_start) &
            (PlayerTeamAvailability.end_time > window_end))
    ).all()

    window_size_hours = 24 * query.window_size_days
    availability = [0] * window_size_hours
    for region in availability_regions:
        region: PlayerTeamAvailability

        # this is the start time relative to the window (as timedelta)
        #relative_start_time = (region.start_time.replace(tzinfo=utc.utc) - window_start)
        #relative_start_hour = int(relative_start_time.total_seconds() // 3600)
        #relative_end_time = (region.end_time.replace(tzinfo=utc.utc) - window_start)
        #relative_end_hour = int(relative_end_time.total_seconds() // 3600)

        relative_start_time = region.start_time - window_start
        relative_start_hour = int(relative_start_time.total_seconds() // 3600)
        relative_end_time = region.end_time - window_start
        relative_end_hour = int(relative_end_time.total_seconds() // 3600)

        i = max(0, relative_start_hour)
        while i < window_size_hours and i < relative_end_hour:
            print(i, "=", region.availability)
            availability[i] = region.availability
            i += 1
    return {
        "availability": availability
    }

class PutScheduleForm(ViewScheduleForm):
    availability: list[int]

def find_consecutive_blocks(arr: list[int]) -> list[tuple[int, int, int]]:
    blocks: list[tuple[int, int, int]] = []
    current_block_value = 0
    current_block_start = 0

    for i in range(len(arr)):
        if arr[i] != current_block_value:
            # we find a different value
            if current_block_value > 0:
                blocks.append((current_block_value, current_block_start, i))
            # begin a new block
            current_block_start = i
        current_block_value = arr[i]

    if current_block_value > 0:
        blocks.append((current_block_value, current_block_start, len(arr)))

    return blocks

@api_schedule.put("/")
@spec.validate()
@requires_authentication
def put(json: PutScheduleForm, player: Player, **kwargs):
    window_start = json.window_start
    window_end = window_start + datetime.timedelta(days=json.window_size_days)

    # TODO: add error message
    if len(json.availability) != 168:
        abort(400, {
            "error": "Availability must be length " + str(168)
        })

    cur_availability = db.session.query(
        PlayerTeamAvailability
    ).where(
        PlayerTeamAvailability.player_id == player.steam_id
    ).where(
        PlayerTeamAvailability.team_id == json.team_id
    ).where(
        PlayerTeamAvailability.start_time.between(window_start, window_end) |
            PlayerTeamAvailability.end_time.between(window_start, window_end)
    ).order_by(
        PlayerTeamAvailability.start_time
    ).all()

    # cut the availability times so that they do not intersect our window
    if len(cur_availability) > 0:
        if cur_availability[0].start_time < window_start:
            if cur_availability[0].end_time > window_end:
                # if the availability overlaps the entire window, duplicate it
                # this way, we can trim the start_time of the duplicate
                cur_availability.append(cur_availability[0])
            cur_availability[0].end_time = window_start
        if cur_availability[-1].end_time > window_end:
            cur_availability[-1].start_time = window_end

    # remove all availability regions strictly inside window
    i = 0
    for region in cur_availability[:]:
        if region.start_time >= window_start and region.end_time <= window_end:
            print("Deleting", region)
            db.session.delete(region)
            cur_availability.pop(i)
        else:
            i += 1

    if len(cur_availability) > 2:
        # this is not supposed to happen
        db.session.rollback()
        raise ValueError()

    # create time regions inside our window based on the availability array
    availability_blocks = []

    for block in find_consecutive_blocks(json.availability):
        availability_value = block[0]
        hour_start = block[1]
        hour_end = block[2]

        abs_start = window_start + datetime.timedelta(hours=hour_start)
        abs_end = window_start + datetime.timedelta(hours=hour_end)

        print("Create availability from", abs_start, "to", abs_end)

        new_availability = PlayerTeamAvailability()
        new_availability.availability = availability_value
        new_availability.start_time = abs_start
        new_availability.end_time = abs_end
        new_availability.player_id = player.steam_id
        new_availability.team_id = json.team_id

        availability_blocks.append(new_availability)

    # merge availability blocks if needed
    if len(cur_availability) > 0 and len(availability_blocks) > 0:
        if availability_blocks[0].start_time == cur_availability[0].end_time:
            cur_availability[0].end_time = availability_blocks[0].end_time
            availability_blocks.pop(0)

    if len(cur_availability) > 0 and len(availability_blocks) > 0:
        if availability_blocks[-1].end_time == cur_availability[-1].start_time:
            cur_availability[-1].start_time = availability_blocks[-1].start_time
            availability_blocks.pop(-1)

    db.session.add_all(availability_blocks)
    db.session.commit()
    return make_response({ }, 200)

class ViewAvailablePlayersForm(BaseModel):
    start_time: datetime.datetime
    team_id: int

@api_schedule.get("/view-available")
@spec.validate()
@requires_authentication
def view_available(query: ViewAvailablePlayersForm, player: Player, **kwargs):
    start_time = query.start_time

    availability = db.session.query(
        PlayerTeamAvailability
    ).where(
        PlayerTeamAvailability.player_id == player.steam_id
    ).where(
        PlayerTeamAvailability.team_id == query.team_id
    ).where(
        (PlayerTeamAvailability.start_time <= start_time) &
            (PlayerTeamAvailability.end_time > start_time)
    ).all()

    def map_roles_to_json(roles: list[PlayerTeamRole],
                          player_team: PlayerTeam,
                          entry: PlayerTeamAvailability):
        for role in roles:
            yield {
                "steamId": entry.player_id,
                "username": entry.player_team.player.username,
                "role": role.role.name,
                "isMain": role.is_main,
                "availability": entry.availability,
                "playtime": int(player_team.playtime.total_seconds()),
            }

    def map_availability_to_json(entry: PlayerTeamAvailability):
        player_team = entry.player_team
        player_roles = player_team.player_roles
        return list(map_roles_to_json(player_roles, player_team, entry))

    return jsonify(list(map(map_availability_to_json, availability)))