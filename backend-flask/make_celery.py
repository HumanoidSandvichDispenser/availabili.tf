from app_db import connect_celery_with_app, app, connect_db_with_app

connect_db_with_app(None, False)
connect_celery_with_app()

celery_app = app.extensions["celery"]

import jobs.fetch_logstf
