import random
import string
import urllib.parse
from flask import Blueprint, abort, make_response, redirect, request, url_for
import requests
import models
from models import AuthSession, Player, db
from middleware import requires_authentication

api_login = Blueprint("login", __name__, url_prefix="/login")

STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"

@api_login.get("/")
def index():
    return "test"

def get_steam_login_url(return_to):
    """Build the Steam OpenID URL for login"""
    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": return_to,
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
    }
    return f"{STEAM_OPENID_URL}?{urllib.parse.urlencode(params)}"

#@api_login.get("/steam/")
#def steam_login():
#    return_to = url_for("api.login.steam_login_callback", _external=True)
#    steam_login_url = get_steam_login_url(return_to)
#    return redirect(steam_login_url)
#
#@api_login.get("/steam/callback/")
#def steam_login_callback():
#    params = request.args.to_dict()
#    params["openid.mode"] = "check_authentication"
#    response = requests.post(STEAM_OPENID_URL, data=params)
#
#    # Check if authentication was successful
#    if "is_valid:true" in response.text:
#        claimed_id = request.args.get("openid.claimed_id")
#        steam_id = extract_steam_id_from_response(claimed_id)
#        print("User logged in as", steam_id)
#
#        player = create_or_get_user_from_steam_id(int(steam_id))
#        auth_session = create_auth_session_for_player(player)
#
#        resp = make_response("Logged in")
#        resp.set_cookie("auth", auth_session.key, secure=True, httponly=True)
#        return resp
#    return "no"

@api_login.post("/authenticate")
def steam_authenticate():
    params = request.get_json()
    params["openid.mode"] = "check_authentication"
    response = requests.post(STEAM_OPENID_URL, data=params)

    # check if authentication was successful
    if "is_valid:true" in response.text:
        claimed_id = params["openid.claimed_id"]
        steam_id = int(extract_steam_id_from_response(claimed_id))
        print("User logged in as", steam_id)

        #player = create_or_get_user_from_steam_id(int(steam_id))
        player = db.session.query(
            Player
        ).where(
            Player.steam_id == steam_id
        ).one_or_none()

        if not player:
            if "username" in params:
                # we are registering, so create user
                player = Player()
                player.username = params["username"]
                player.steam_id = steam_id
            else:
                # prompt client to resend with username field
                return make_response({
                    "message": "Awaiting registration",
                    "hint": "Resend the POST request with a username field",
                    "isRegistering": True,
                })

        auth_session = create_auth_session_for_player(player)

        resp = make_response({
            "message": "Logged in",
            "steamId": player.steam_id,
            "username": player.username,
        })

        # TODO: secure=True in production
        resp.set_cookie("auth", auth_session.key, httponly=True)
        return resp
    return abort(401)

@api_login.delete("/")
@requires_authentication
def logout(**kwargs):
    auth_session: AuthSession = kwargs["auth_session"]
    db.session.delete(auth_session)
    response = make_response(200)
    response.delete_cookie("auth")
    return response

def create_or_get_user_from_steam_id(steam_id: int, username: str) -> Player:
    statement = db.select(Player).filter_by(steam_id=steam_id)
    player = db.session.execute(statement).scalar_one_or_none()
    if not player:
        player = Player()
        player.steam_id = steam_id
        player.username = username
        db.session.add(player)
        db.session.commit()
    return player

def generate_base36(length):
    alphabet = string.digits + string.ascii_uppercase
    return "".join(random.choice(alphabet) for _ in range(length))

def create_auth_session_for_player(player: models.Player):
    session = AuthSession()
    session.player = player

    random_key = generate_base36(31)
    session.key = random_key

    player.auth_sessions.append(session)
    db.session.commit()
    return session

def extract_steam_id_from_response(claimed_id_url):
    return claimed_id_url.split("/")[-1]
