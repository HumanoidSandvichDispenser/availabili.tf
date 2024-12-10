from models.player import Player
from models.team import Team
from models.player_team import PlayerTeam
from models.team_integration import TeamDiscordIntegration, TeamLogsTfIntegration
from flask_testing import TestCase
from app_db import app, db, connect_db_with_app

SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
connect_db_with_app(SQLALCHEMY_DATABASE_URI, False)


class BaseTestCase(TestCase):
    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        self.populate_db()
        return app

    def tearDown(self):
        from app_db import db
        db.session.remove()
        db.drop_all()

    def populate_db(self):
        print(list(map(lambda x: x.username, db.session.query(Player).all())))
        player = Player(steam_id=76561198248436608, username="pyro from csgo")
        team = Team(team_name="Team Pepeja", tz_timezone="America/New_York", minute_offset=30)

        db.session.add(player)
        db.session.add(team)

        db.session.flush()
        

        player_team = PlayerTeam(
            player_id=player.steam_id,
            team_id=team.id,
            team_role=PlayerTeam.TeamRole.Player,
            is_team_leader=True,
        )
        logs_tf_integration = TeamLogsTfIntegration(
            team_id=team.id,
            min_team_member_count=2,
        )

        db.session.add(player_team)
        db.session.add(logs_tf_integration)

        db.session.commit()
