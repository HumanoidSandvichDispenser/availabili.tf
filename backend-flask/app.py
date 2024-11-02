from flask import Blueprint, Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import login
import schedule
import team
from models import init_db

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
CORS(login.api_login, origins=["http://localhost:5173"], supports_credentials=True)
CORS(schedule.api_schedule, origins=["http://localhost:5173"], supports_credentials=True)

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
