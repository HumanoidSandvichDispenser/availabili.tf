#from typing import cast, override
from typing import TypeAlias, Union
from pydantic_core.core_schema import UnionSchema
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.types import Integer, String
import app_db
import spec


class TeamIntegration(app_db.BaseModel):
    __tablename__ = "team_integrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id"))
    integration_type: Mapped[str]

    team: Mapped["Team"] = relationship(back_populates="integrations")

    __mapper_args__ = {
        "polymorphic_identity": "team_integrations",
        "polymorphic_on": "integration_type",
    }

class TeamDiscordIntegration(TeamIntegration):
    __tablename__ = "team_discord_integrations"

    integration_id: Mapped[int] = mapped_column(ForeignKey("team_integrations.id"), primary_key=True)
    webhook_url: Mapped[str] = mapped_column(String(255), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "team_discord_integrations",
    }

class TeamIntegrationSchema(spec.BaseModel):
    id: int
    team_id: int
    integration_type: str

    @classmethod
    def from_model(cls, model: TeamIntegration):
        if model.integration_type == "team_discord_integrations":
            if isinstance(model, TeamDiscordIntegration):
                return TeamDiscordIntegrationSchema._from_model_discord(model)
        raise TypeError()

class TeamDiscordIntegrationSchema(TeamIntegrationSchema):
    webhook_url: str

    @classmethod
    def _from_model_discord(cls, model: TeamDiscordIntegration):
        assert model.integration_id != None
        return cls(
            id=model.integration_id,
            team_id=model.team_id,
            integration_type=model.integration_type,
            webhook_url=model.webhook_url
        )

class ExampleIntegrationSchema(TeamIntegrationSchema):
    test: str

class AbstractTeamIntegrationSchema(spec.BaseModel):
    __root__: TeamDiscordIntegrationSchema | TeamIntegrationSchema


from models.team import Team
