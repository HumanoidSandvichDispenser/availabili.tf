from flask import Blueprint, Flask, make_response, request

import login
import schedule
import team
from models import init_db
from spec import spec

app = Flask(__name__)

init_db(app)

api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(login.api_login)
api.register_blueprint(schedule.api_schedule)
api.register_blueprint(team.api_team)

@api.get("/debug/set-cookie")
@api.post("/debug/set-cookie")
def debug_set_cookie():
    res = make_response()
    for key, value in request.args.items():
        res.set_cookie(key, value)
    return res, 200

app.register_blueprint(api)
spec.register(app)
