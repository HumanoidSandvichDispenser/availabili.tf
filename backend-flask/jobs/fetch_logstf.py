from collections.abc import Generator
from datetime import timedelta, datetime
from time import sleep
import requests
from sqlalchemy.sql import exists, func, select, update
from sqlalchemy.types import DATETIME, Interval
import app_db
import models.match
from models.match import Match
from models.team_match import TeamMatch
from models.player import Player
from models.player_match import PlayerMatch
from models.player_team import PlayerTeam
from models.team_integration import TeamLogsTfIntegration
from celery import shared_task

celery = app_db.connect_celery_with_app()

@celery.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(300.0, etl_periodic.s(), name="Fetch logs every 5 minutes")

FETCH_URL = "https://logs.tf/api/v1/log/{}"
SEARCH_URL = "https://logs.tf/api/v1/log?limit=25?offset={}"


def get_log_ids(last_log_id: int):
    current: int = 2147483647
    while current > last_log_id:
        response = requests.get(SEARCH_URL.format(current))
        for summary in response.json()["logs"]:
            id: int = summary["id"]
            if id == last_log_id:
                print("Reached last log ID", id)
                return
            # yield models.match.RawLogSummary.from_response(summary)
            yield id
            current = id
        sleep(5)
        break

def extract(log_id: int) -> models.match.RawLogDetails:
    response = requests.get(FETCH_URL.format(log_id))
    return response.json()

def steam3_to_steam64(steam3_id: str) -> int:
    if steam3_id.startswith("[U:1:") and steam3_id.endswith("]"):
        numeric_id = int(steam3_id[5:-1])
        steam64_id = numeric_id + 76561197960265728
        return steam64_id
    else:
        raise ValueError("Invalid Steam3 ID format")

def steam64_to_steam3(steam64_id: int) -> str:
    if steam64_id >= 76561197960265728:
        numeric_id = steam64_id - 76561197960265728
        steam3_id = f"[U:1:{numeric_id}]"
        return steam3_id
    else:
        raise ValueError("Invalid Steam64 ID format")

def extract_steam_ids(players: dict[str, models.match.LogPlayer]):
    blue_steam_ids: list[int] = []
    red_steam_ids: list[int] = []
    steam_ids: list[int] = []

    for steam_id, player in players.items():
        steam64_id = steam3_to_steam64(steam_id)
        steam_ids.append(steam64_id)
        if player["team"] == "Red":
            red_steam_ids.append(steam64_id)
        elif player["team"] == "Blue":
            blue_steam_ids.append(steam64_id)

    return steam_ids, blue_steam_ids, red_steam_ids

@shared_task
def update_playtime(steam_ids: list[int]):
    #steam_ids_int = list(map(lambda x: int(x), steam_ids))
    ptp = (
        select(
            PlayerTeam.id.label("id"),
            func.sum(Match.duration).label("playtime")
        )
        .select_from(PlayerTeam)
        .join(PlayerMatch, PlayerMatch.player_id == PlayerTeam.player_id)
        .join(Match, PlayerMatch.match_id == Match.logs_tf_id)
        .join(TeamMatch, TeamMatch.match_id == Match.logs_tf_id)
        .where(
            PlayerTeam.player_id.in_(steam_ids),
            PlayerTeam.team_id == TeamMatch.team_id
        )
        .group_by(PlayerTeam.id)
        .cte("ptp")
    )

    stmt = (
        update(PlayerTeam)
        .values(
            playtime=(
                select(ptp.c.playtime)
                .where(PlayerTeam.id == ptp.c.id)
            )
        )
        .where(
            exists(
                select(1)
                .select_from(ptp)
                .where(PlayerTeam.id == ptp.c.id)
            )
        )
    )

    print(stmt)

    app_db.db.session.execute(stmt)
    app_db.db.session.commit()


def get_common_teams(steam_ids: list[int]):
    return (
        app_db.db.session.query(
            PlayerTeam.team_id,
            func.count(PlayerTeam.team_id),
            #aggregate_func
        )
        .where(PlayerTeam.player_id.in_(steam_ids))
        .group_by(PlayerTeam.team_id)
        .order_by(func.count(PlayerTeam.team_id).desc())
        .all()
    )

def transform(
    log_id: int,
    details: models.match.RawLogDetails,
    existing_match: Match | None = None,
    invoked_by_team_id: int | None = None
):
    steam_ids, blue_steam_ids, red_steam_ids = extract_steam_ids(details["players"])

    # fetch players in steam_ids if they exist
    players = (
        app_db.db.session.query(Player)
        .where(Player.steam_id.in_(steam_ids))
        .all()
    )

    if not existing_match:
        match = Match()
        match.logs_tf_id = log_id
        match.logs_tf_title = details["info"]["title"]
        match.blue_score = details["teams"]["Blue"]["score"]
        match.red_score = details["teams"]["Red"]["score"]
        match.duration = details["length"]
        match.match_time = datetime.fromtimestamp(details["info"]["date"])
        yield match
    else:
        match = existing_match

    if len(players) == 0:
        return

    for player in players:
        player_data = details["players"][steam64_to_steam3(player.steam_id)]

        if not player_data:
            print(f"Player {player.steam_id} not found in log {log_id}")
            continue

        player_match = PlayerMatch()
        player_match.player_id = player.steam_id
        player_match.match_id = match.logs_tf_id
        player_match.kills = player_data["kills"]
        player_match.deaths = player_data["deaths"]
        player_match.assists = player_data["assists"]
        player_match.damage = player_data["dmg"]
        player_match.damage_taken = player_data["dt"]

        yield player_match

    # get common teams
    # if common teams exist, automatically create a TeamMatch for the match
    for team, ids in { "Blue": blue_steam_ids, "Red": red_steam_ids }.items():
        for row in get_common_teams(ids):
            row_tuple = tuple(row)
            team_id = row_tuple[0]
            player_count = row_tuple[1]
            logs_integration = app_db.db.session.query(
                TeamLogsTfIntegration
            ).where(TeamLogsTfIntegration.team_id == team_id).one_or_none()

            log_min_player_count = 100
            if logs_integration:
                log_min_player_count = logs_integration.min_team_member_count

            should_create_team_match = False


            if invoked_by_team_id and team_id == invoked_by_team_id:
                # if manually uploading a log, then add TeamMatch for the team
                # that uploaded the log
                should_create_team_match = True
            elif not invoked_by_team_id and player_count >= log_min_player_count:
                # if automatically fetching logs, then add TeamMatch for teams
                # with player count >= log_min_player_count
                should_create_team_match = True

            if should_create_team_match:
                team_match = TeamMatch()
                team_match.team_id = team_id
                team_match.match_id = match.logs_tf_id
                team_match.team_color = team
                yield team_match

    #app_db.db.session.flush()
    update_playtime.delay(steam_ids)


@shared_task
def load_specific_match(id: int, team_id: int | None):
    match = (
        app_db.db.session.query(Match)
        .where(Match.logs_tf_id == id)
        .first()
    )

    raw_match = extract(id)
    print("Loading match: " + str(id))
    app_db.db.session.bulk_save_objects(transform(id, raw_match, match, team_id))
    app_db.db.session.commit()
    sleep(3)  # avoid rate limiting if multiple tasks are queued


@celery.task
def etl_periodic():
    last: int = (
        app_db.db.session.query(
            func.max(models.match.Match.logs_tf_id)
        ).scalar()
    ) or 3768715

    print("Last log ID: " + str(last))

    for id in get_log_ids(last):
        print("Found log: " + str(id))
        load_specific_match.delay(id, None)
