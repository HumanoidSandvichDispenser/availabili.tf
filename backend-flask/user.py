import os
from flask import Blueprint, abort, make_response, request
import requests
from spectree import Response
from middleware import requires_admin, requires_authentication
from models.player import Player, PlayerSchema
from spec import spec, BaseModel
from app_db import db


api_user = Blueprint("user", __name__, url_prefix="/user")

# TODO: use env vars
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_CLIENT_ID = "1372254613692219392" #os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")

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

#class DiscordAuthQuery(BaseModel):
#    code: str
#    redirect_uri: str
#
#@api_user.post("/discord-authenticate")
#@spec.validate(
#    operation_id="discord_authenticate"
#)
#@requires_authentication
#def discord_authenticate(query: DiscordAuthQuery, player: Player, **_):
#    if not DISCORD_CLIENT_ID or not DISCORD_CLIENT_SECRET:
#        abort(500, "The site is not configured to use Discord authentication")
#
#    data = {
#        "client_id": DISCORD_CLIENT_ID,
#        "client_secret": DISCORD_CLIENT_SECRET,
#        "grant_type": "authorization_code",
#        "code": query.code,
#        "redirect_uri": query.redirect_uri,
#        "scope": "identify"
#    }
#    response = requests.post(DISCORD_TOKEN_URL, data)
#    access_token = response.json()["access_token"]
#
#    headers = {
#        "authorization": f"Bearer {access_token}"
#    }
#    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
#
#    id = response.json()[]
