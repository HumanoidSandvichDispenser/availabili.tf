from flask import Blueprint
from spectree import Response
from middleware import requires_authentication
from models.player import Player, PlayerSchema
from spec import spec, BaseModel
from app_db import db


api_user = Blueprint("user", __name__, url_prefix="/user")

class SetUsernameJson(BaseModel):
    username: str

@api_user.post("username")
@spec.validate(
    resp=Response(
        HTTP_200=PlayerSchema,
    ),
    operation_id="set_username",
)
@requires_authentication
def set_username(json: SetUsernameJson, player: Player, **kwargs):
    player.username = json.username
    db.session.commit()
    return PlayerSchema.from_model(player).dict(by_alias=True), 200
