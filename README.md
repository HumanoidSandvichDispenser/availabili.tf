# availabili.tf

Scheduling for TF2

## Tech Stack

- **Frontend:** [Vue 3](https://v3.vuejs.org/) + TypeScript
    - **State Management:** [Pinia](https://pinia.vuejs.org/)
- **Backend:** [Flask](https://flask.palletsprojects.com/) + Python
    - **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
    - **Validation:** [Pydantic](https://pydantic-docs.helpmanual.io/)
    - [spectree](https://spectree.readthedocs.io/en/latest/index.html) for
      OpenAPI documentation
    - [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
      (Alembic) for database migrations
    - [Celery](https://docs.celeryproject.org/en/stable/) for async tasks
    - [Redis](https://redis.io/) for Celery broker
- **Database:** [PostgreSQL 17.1](https://www.postgresql.org/docs/17/index.html)
  (production) / SQLite (development)

## Setup (dev)

```sh
docker compose build
docker compose up
DATABASE_URI=sqlite:///db.sqlite3 flask db upgrade
```

App will run at port 8000.

## Setup (production)

Build the frontend app:

```sh
cd availabili.tf
npm run build
```

Build the rest of the containers:

```sh
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up
```

Perform initial database migration:

```sh
docker exec -it backend bash
flask db upgrade
```

## OpenAPI

The backend will automatically serve its OpenAPI-compliant spec at
`/apidoc/openapi.json` which can also be viewed at `/apidoc/redoc` or
`/apidoc/swagger` or `/apidoc/scalar`.

To generate the frontend client:

```sh
npm run openapi-generate
```
