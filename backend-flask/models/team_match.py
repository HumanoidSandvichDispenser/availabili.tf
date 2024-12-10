from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Integer, String
import app_db
import spec


class TeamMatch(app_db.BaseModel):
    __tablename__ = "teams_matches"

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.logs_tf_id"), primary_key=True)
    team_color: Mapped[str] = mapped_column(String(4))

    team: Mapped["Team"] = relationship("Team", back_populates="matches")
    match: Mapped["Match"] = relationship("Match", back_populates="teams")

class TeamMatchSchema(spec.BaseModel):
    match: "MatchSchema"
    our_score: int
    their_score: int

    @classmethod
    def from_model(cls, model: "TeamMatch"):
        our_score = model.match.blue_score if model.team_color == "Blue" else model.match.red_score
        their_score = model.match.red_score if model.team_color == "Blue" else model.match.blue_score

        return cls(
            match=MatchSchema.from_model(model.match),
            our_score=our_score,
            their_score=their_score,
        )


from models.match import Match, MatchSchema
from models.team import Team
