# Project Structure

This boilerplate uses a domain-module layout. Each feature owns its model, schema, service, and route files so new functionality can be added without crowding global modules.

## Current Layout

```text
app/
├── __init__.py
├── main.py
├── config.py
├── database.py
├── scheduler.py
├── api/
│   ├── __init__.py
│   └── routes.py
└── users/
    ├── __init__.py
    ├── models.py
    ├── schemas.py
    ├── services.py
    └── routes.py
```

## Responsibilities

`app/main.py`
: Creates the FastAPI app, registers middleware, registers routers, and runs startup work through the lifespan hook.

`app/config.py`
: Defines typed settings loaded from environment variables and `.env`.

`app/database.py`
: Creates the SQLAlchemy engine, session factory, declarative base, and request-scoped database dependency.

`app/api/routes.py`
: Aggregates feature routers under the API prefix configured by `API_V1_PREFIX`.

`app/<feature>/models.py`
: SQLAlchemy table definitions and relationships.

`app/<feature>/schemas.py`
: Pydantic request and response models.

`app/<feature>/services.py`
: Business rules and database operations.

`app/<feature>/routes.py`
: HTTP endpoint definitions. Keep this layer thin and delegate real work to services.

## Adding A Module

1. Create `app/<feature>/__init__.py`.
2. Add database tables in `models.py`.
3. Add request and response DTOs in `schemas.py`.
4. Add business logic in `services.py`.
5. Add route handlers in `routes.py`.
6. Register the router in `app/api/routes.py`.
7. Add focused tests under `tests/`.

Example router registration:

```python
from app.posts.routes import router as posts_router

api_router.include_router(posts_router)
```

## Request Flow

```text
HTTP request
  -> route
  -> service
  -> model/session
  -> database
  -> response schema
```

This keeps HTTP concerns, business rules, and persistence concerns separate while staying simple enough for a starter project.
