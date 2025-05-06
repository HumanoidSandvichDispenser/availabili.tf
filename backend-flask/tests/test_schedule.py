import datetime
import app_db
from models.player_team_availability import PlayerTeamAvailability
from models.player_team_role import PlayerTeamRole


def test_get_schedule_7days_168elements(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.get(
        "/api/schedule/team?windowStart=0&teamId=1&windowSizeDays=7",
        headers=headers)
    assert len(response.json["playerAvailability"]["76561198248436608"]["availability"]) == 168

def test_find_consecutive_blocks_len_1():
    from schedule import find_consecutive_blocks

    blocks = find_consecutive_blocks([0, 1, 1, 1, 0])
    assert len(blocks) == 1

def test_find_consecutive_blocks_len_2():
    from schedule import find_consecutive_blocks

    blocks = find_consecutive_blocks([0, 1, 0, 1, 0])
    assert len(blocks) == 2

def test_find_consecutive_blocks_size_4():
    from schedule import find_consecutive_blocks

    blocks = find_consecutive_blocks([0, 2, 2, 2, 2])
    print(blocks)
    assert blocks[0][2] - blocks[0][1] == 4

def test_get_team_availability(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.get(
        "/api/schedule/team?windowStart=0&teamId=1&windowSizeDays=7",
        headers=headers)
    assert len(response.json["playerAvailability"]) == 1

def test_view_available_at_time_not_available(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.get(
        "/api/schedule/view-available?teamId=1&startTime=2024-10-01T00:00:00Z",
        headers=headers)
    assert len(response.json["players"]) == 0

def test_view_available_at_time_is_available(client, headers):
    client.set_cookie("auth", "test_key")

    pta = PlayerTeamAvailability(
        player_team_id=1,
        start_time=datetime.datetime(2024, 9, 1, 0, 0, tzinfo=datetime.timezone.utc),
        end_time=datetime.datetime(2024, 10, 5, 2, 0, tzinfo=datetime.timezone.utc),
    )

    app_db.db.session.add(pta)

    ptr = PlayerTeamRole(
        player_team_id=1,
        role=PlayerTeamRole.Role.Pyro,
        is_main=True,
    )

    app_db.db.session.add(ptr)
    app_db.db.session.commit()

    response = client.get(
        "/api/schedule/view-available?teamId=1&startTime=1727740800",
        headers=headers)
    print(response.json)
    assert len(response.json["players"]) == 1
