from datetime import timedelta
from base_test_case import BaseTestCase

from app_db import db
from models.match import Match, RawLogDetails
from models.player import Player
from models.player_match import PlayerMatch
from models.player_team import PlayerTeam
from models.team_match import TeamMatch


class TestLogstfJob(BaseTestCase):
    def populate_db(self):
        from app_db import db

        super().populate_db()

        wesker_u = Player(steam_id=76561198024482308, username="Wesker U")
        wesker_u_pt = PlayerTeam(
            player_id=wesker_u.steam_id,
            team_id=1,
            team_role=PlayerTeam.TeamRole.Player,
            is_team_leader=True,
        )

        db.session.add(wesker_u)
        db.session.add(wesker_u_pt)

        db.session.commit()

    def test_get_common_teams(self):
        from jobs.fetch_logstf import get_common_teams

        rows = get_common_teams([76561198248436608, 76561198024482308])
        assert len(rows) == 1
        assert rows == [(1, 2, 2)]

    def test_transform(self):
        from jobs.fetch_logstf import transform

        details: RawLogDetails = {
            "players": {
                "[U:1:288170880]": {
                    "team": "Red",
                    "kills": 1,
                    "deaths": 2,
                    "assists": 3,
                    "dmg": 4,
                    "dt": 5,
                },
                "[U:1:64216580]": {
                    "team": "Red",
                    "kills": 6,
                    "deaths": 7,
                    "assists": 8,
                    "dmg": 9,
                    "dt": 10,
                },
                "[U:1:64216581]": {
                    "team": "Blue",
                    "kills": 6,
                    "deaths": 7,
                    "assists": 8,
                    "dmg": 9,
                    "dt": 10,
                },
            },
            "info": {
                "title": "I LOVE DUSTBOWL",
                "map": "cp_dustbowl",
                "date": 1614547200,
            },
            "teams": {
                "Blue": {
                    "score": 1
                },
                "Red": {
                    "score": 2
                }
            },
            "length": 3025,
        }

        for instance in transform(1, details):
            db.session.add(instance)
        db.session.commit()

        assert db.session.query(Player).count() == 2
        assert db.session.query(PlayerMatch).count() == 2
        assert db.session.query(TeamMatch).count() == 1
        assert db.session.query(Match).count() == 1
        assert db.session.query(PlayerTeam).count() == 2
        player_team = db.session.query(PlayerTeam).first()
        assert player_team is not None
        print(player_team.playtime)
        assert player_team.playtime == 3025

    def test_steam3_to_steam64(self):
        from jobs.fetch_logstf import steam3_to_steam64
        assert steam3_to_steam64("[U:1:123456]") == 76561197960265728 + 123456

    def test_steam64_to_steam3(self):
        from jobs.fetch_logstf import steam64_to_steam3
        assert steam64_to_steam3(76561197960265728 + 123456) == "[U:1:123456]"
