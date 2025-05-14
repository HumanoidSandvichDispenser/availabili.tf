from flask import Blueprint, abort, make_response
from spectree import Response
from middleware import requires_admin, requires_authentication
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

@api_user.get("/all")
@spec.validate(
    resp=Response(
        HTTP_200=list[PlayerSchema],
    ),
    operation_id="get_all_users",
)
@requires_authentication
@requires_admin
def get_all_users(player: Player, **kwargs):
    players = db.session.query(Player).all()
    return list(map(lambda p: PlayerSchema.from_model(p).dict(by_alias=True), players)), 200

@api_user.put("/doas/<steam_id>")
@spec.validate(
    resp=Response(
        HTTP_200=PlayerSchema,
    ),
    operation_id="set_doas"
)
@requires_authentication
@requires_admin
def set_doas(steam_id: str, **_):
    try:
        steam_id_int = int(steam_id)
    except ValueError:
        abort(400, "steam_id must be an integer")

    player = db.session.query(Player).where(
        Player.steam_id == steam_id_int
    ).one_or_none()

    if not player:
        abort(404)

    resp = make_response(
        PlayerSchema.from_model(player).dict(by_alias=True)
    )
    resp.set_cookie("doas", steam_id, httponly=True)
    return resp

@api_user.delete("/doas")
@spec.validate(
    resp=Response(
        HTTP_204=None,
    ),
    operation_id="unset_doas"
)
@requires_authentication
@requires_admin
def unset_doas(**_):
    resp = make_response({ }, 204)
    resp.delete_cookie("doas", httponly=True)
    return resp
