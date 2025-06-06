from flask import Blueprint, make_response, request
import flask_migrate

from app_db import app, connect_celery_with_app, connect_db_with_app
import login
import schedule
import team
from spec import spec
import user
import events
import match

connect_db_with_app(None)
connect_celery_with_app()

api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(login.api_login)
api.register_blueprint(schedule.api_schedule)
api.register_blueprint(team.api_team)
api.register_blueprint(user.api_user)
api.register_blueprint(events.api_events)
api.register_blueprint(match.api_match)

@api.get("/debug/set-cookie")
@api.post("/debug/set-cookie")
def debug_set_cookie():
    res = make_response()
    for key, value in request.args.items():
        res.set_cookie(key, value)
    return res, 200

app.register_blueprint(api)
spec.register(app)
