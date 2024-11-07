from datetime import timedelta
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
        resp.set_cookie(
            "auth",
            auth_session.key,
            httponly=True,
            max_age=timedelta(days=30),
        )
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
