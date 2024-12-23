from os import environ
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from celery import Celery, Task

class BaseModel(DeclarativeBase):
    pass

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

def connect_db_with_app(database_uri: str | None, include_migrate=True):
    database_uri = database_uri or environ.get("DATABASE_URI")
    if not database_uri:
        raise ValueError("Database URI is not provided")
    print("Connecting to database: " + database_uri)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    db.init_app(app)
    if include_migrate:
        migrate.init_app(app, db)
    with app.app_context():
        print("Running dialect: " + db.engine.dialect.name)

    import models as _
    if environ.get("FLASK_ENV") == "production":
        print("Creating tables if they do not exist")
        db.create_all()

def connect_celery_with_app() -> Celery:
    if "celery" in app.extensions:
        return app.extensions["celery"]

    def celery_init_app(app):
        class FlaskTask(Task):
            def __call__(self, *args: object, **kwargs: object) -> object:
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery_app = Celery(app.name, task_cls=FlaskTask, broker=app.config["CELERY"]["broker_url"])
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
        app.extensions["celery"] = celery_app
        return celery_app

    app.config.from_mapping(
        CELERY=dict(
            broker_url=environ.get("CELERY_BROKER_URL", "redis://redis:6379/0"),
            result_backend=environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
            task_ignore_result=True,
        )
    )
    app.config.from_prefixed_env()
    return celery_init_app(app)

def create_app() -> Flask:
    return Flask(__name__)

metadata = MetaData(naming_convention=convention)
app = create_app()
db = SQLAlchemy(model_class=BaseModel, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
