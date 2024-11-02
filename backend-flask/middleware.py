from functools import wraps
from flask import abort, make_response, request
from models import db
import models


def requires_authentication(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.cookies.get("auth")

        if not auth:
            abort(401)

        statement = db.select(models.AuthSession).filter_by(key=auth)
        auth_session: models.AuthSession | None = \
            db.session.execute(statement).scalar_one_or_none()

        if not auth_session:
            abort(make_response({
                "error": "Invalid auth token"
            }, 401))
        player = auth_session.player
        kwargs["player"] = player
        kwargs["auth_session"] = auth_session
        return f(*args, **kwargs)
    return decorator
