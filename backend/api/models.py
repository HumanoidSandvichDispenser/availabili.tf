from typing import override
from django.db import models
from cpkmodel import CPkModel
from django.db.models.constraints import UniqueConstraint

class Team(models.Model):
    team_name = models.CharField(max_length=63)

    @override
    def __str__(self) -> str:
        return str(self.team_name)

class Player(models.Model):
    steam_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=63)

    @override
    def __str__(self) -> str:
        return f"{self.name}#{self.steam_id}"

class PlayerInfo(models.Model):
    player = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        null=False,
        primary_key=True
    )
    team = models.ManyToManyField(Team, through="PlayerInfo_Team")

    @override
    def __str__(self) -> str:
        return str(self.player)

class PlayerInfo_Team(models.Model):
    class TeamRole(models.TextChoices):
        PLAYER = "PL", "Player"
        COACH_MENTOR = "CM", "Coach/Mentor"
        TEAM_LEADER = "TL", "Team Leader"

    player_info = models.ForeignKey(PlayerInfo, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    team_role = models.CharField(
        max_length=2,
        choices=TeamRole.choices,
        default=TeamRole.PLAYER
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @override
    def __str__(self) -> str:
        return f"{self.player_info} in {self.team} as {self.team_role}"

    class Meta:
        unique_together = (("player_info", "team"),)

class PlayerRole(models.Model):
    class Role(models.TextChoices):
        P_SCOUT = "P_SCOUT", "Pocket Scout"
        F_SCOUT = "F_SCOUT", "Flank Scout"
        SCOUT = "SCOUT", "Scout"

        P_SOLLY = "P_SOLLY", "Pocket Soldier"
        ROAMER = "ROAMER", "Roamer"
        SOLDIER = "SOLDIER", "Soldier"

        PYRO = "PYRO", "Pyro"
        DEMO = "DEMO", "Demoman"
        HEAVY = "HEAVY", "Heavy"
        ENGIE = "ENGIE", "Engineer"
        MEDIC = "MEDIC", "Medic"
        SNIPER = "SNIPER", "Sniper"
        SPY = "SPY", "Spy"

    playerinfo_team = models.ForeignKey(
        PlayerInfo_Team,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    player_role = models.CharField(
        max_length=7,
        choices=Role.choices,
    )
    main = models.BooleanField(default=True)

    @override
    def __str__(self) -> str:
        return f"{self.playerinfo_team.player_info} ({self.player_role} for {self.playerinfo_team.team})"

class PlayerTeamAvailability(models.Model):
    player_info_team = models.ForeignKey(PlayerInfo_Team, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.SmallIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=[
                "player_info_team",
                "start_time"
            ], name="unique_team_availability")
        ]

    @override
    def __str__(self) -> str:
        return f"{self.player_info_team} available on {self.start_time}"

class PlayerMasterAvailability(models.Model):
    player_info = models.ForeignKey(PlayerInfo, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.SmallIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=[
                "player_info",
                "start_time"
            ], name="unique_master_availability")
        ]

    @override
    def __str__(self) -> str:
        return f"{self.player_info} available on {self.start_time}"
