# FastAPI Boilerplate

A small, production-shaped FastAPI starter with SQLAlchemy, PostgreSQL, Docker Compose, typed settings, a sample user module, and basic tests.

## What You Get

- FastAPI app factory with `/`, `/health`, Swagger UI, and ReDoc
- Versioned API routing under `/api/v1`
- PostgreSQL through SQLAlchemy 2.x
- Pydantic settings loaded from `.env`
- Docker Compose for API, database, PgAdmin, and an optional scheduler
- Example `users` module with models, schemas, routes, and services
- Password hashing, input validation, duplicate handling, and CRUD tests
- Ruff and pytest configuration in `pyproject.toml`

## Quick Start With Docker

```bash
cp .env.example .env
docker compose up --build
```

Open:

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- PgAdmin: http://localhost:8888

Default PgAdmin login comes from `.env.example`:

- Email: `admin@example.com`
- Password: `admin`

Inside PgAdmin, connect to PostgreSQL with:

- Host: `postgres`
- Port: `5432`
- Database: `app_db`
- Username: `postgres`
- Password: `postgres`

## Local Development

Run PostgreSQL yourself or keep only the database container running:

```bash
docker compose up postgres
```

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

If you run the API outside Docker, set `DATABASE_URL` to a localhost database URL:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/app_db
```

Start the API:

```bash
uvicorn app.main:app --reload
```

## Common Commands

```bash
pytest
ruff check .
ruff format .
docker compose down
docker compose down -v  # also deletes local database volumes
```

## API Endpoints

- `GET /` - API welcome payload
- `GET /health` - health check
- `POST /api/v1/users` - create a user
- `GET /api/v1/users` - list users
- `GET /api/v1/users/{user_id}` - fetch a user
- `PATCH /api/v1/users/{user_id}` - update a user
- `DELETE /api/v1/users/{user_id}` - delete a user

## Configuration

Settings are defined in `app/config.py` and loaded from environment variables.

Important variables:

```env
APP_NAME=FastAPI Boilerplate
ENVIRONMENT=development
DEBUG=true
API_V1_PREFIX=/api/v1
DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/app_db
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

`docker-compose.yml` has defaults, so the app can start without a `.env` file. Copying `.env.example` is still recommended so each project has explicit local settings.

## Project Layout

```text
app/
├── main.py              # FastAPI app factory and lifespan setup
├── config.py            # Environment-based settings
├── database.py          # SQLAlchemy engine, session, and Base
├── scheduler.py         # Optional standalone scheduler process
├── api/
│   └── routes.py        # API router aggregation
└── users/
    ├── models.py        # SQLAlchemy model
    ├── schemas.py       # Pydantic request/response models
    ├── services.py      # Business logic and persistence operations
    └── routes.py        # HTTP endpoints
```

## Adding A Feature Module

Create a new folder under `app/`, for example `app/posts/`, with the same shape as `app/users/`:

```text
app/posts/
├── __init__.py
├── models.py
├── schemas.py
├── services.py
└── routes.py
```

Then register the router in `app/api/routes.py`:

```python
from app.posts.routes import router as posts_router

api_router.include_router(posts_router)
```

Keep route handlers thin. Put validation that belongs to HTTP in `routes.py`, business rules and database writes in `services.py`, and table definitions in `models.py`.

## Database Migrations

This starter creates tables automatically on startup for convenience. For a real production app, wire Alembic into deployment and disable automatic table creation.

Basic Alembic flow:

```bash
alembic init alembic
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

## Production Notes

- Set `ENVIRONMENT=production` and `DEBUG=false`
- Replace broad local CORS origins with your actual frontend origins
- Run migrations with Alembic instead of relying on startup table creation
- Use a managed secret store or deployment platform variables for credentials
- Consider running with Gunicorn:

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 60
```
