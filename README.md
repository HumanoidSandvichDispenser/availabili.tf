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
- **Database:** [PostgreSQL 17.1](https://www.postgresql.org/docs/17/index.html)
  (production) / SQLite (development)

## Setup (dev)

```sh
docker compose up
```

App will run at port 8000.

## OpenAPI

The backend will automatically serve its OpenAPI-compliant spec at
`/apidoc/openapi.json` which can also be viewed at `/apidoc/redoc` or
`/apidoc/swagger` or `/apidoc/scalar`.

To generate the frontend client:

```sh
npm run openapi-generate
```
