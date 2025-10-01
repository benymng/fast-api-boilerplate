# Alira Backend

FastAPI backend application with SQLAlchemy ORM and PostgreSQL database, fully containerized with Docker.

## Features

- ⚡ **FastAPI** - Modern, fast web framework for building APIs
- 🗄️ **SQLAlchemy** - Powerful SQL toolkit and ORM
- 🐘 **PostgreSQL** - Robust relational database
- 🐳 **Docker** - Containerized application with Docker Compose
- 🔧 **PgAdmin** - Web-based PostgreSQL administration tool
- ⏰ **Scheduler** - Optional background task scheduler (APScheduler)
- 📝 **Auto Documentation** - Interactive API docs (Swagger UI & ReDoc)

## Project Structure

```
alira-backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── config.py        # Configuration and settings
│   ├── database.py      # Database connection and session
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas for validation
│   └── scheduler.py     # Background tasks scheduler
├── .env                 # Environment variables (created from .env.example)
├── .env.example         # Example environment variables
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Clone the repository** (if applicable)
   ```bash
   git clone <repository-url>
   cd alira-backend
   ```

2. **Set up environment variables**

3. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```

4. **Access the services**
   - **API**: http://localhost:8000
   - **API Documentation (Swagger)**: http://localhost:8000/docs
   - **API Documentation (ReDoc)**: http://localhost:8000/redoc
   - **PgAdmin**: http://localhost:8888
     - Email: `admin@alira.com`
     - Password: `admin`

## Services

### Web (FastAPI)
- Main API application
- Hot-reload enabled for development
- Runs on port 8000

### PostgreSQL
- Database service
- Persistent data storage with Docker volumes
- Runs on port 5432

### PgAdmin
- Web-based database administration
- Runs on port 8888
- Connect to database using:
  - Host: `postgres`
  - Port: `5432`
  - Database: `alira_db` (or your DATABASE_NAME)
  - Username: `postgres` (or your DATABASE_USER)
  - Password: `postgres` (or your DATABASE_PASSWORD)

### Scheduler (Optional)
- Background task scheduler
- Uncomment in docker-compose.yml if needed
- Runs scheduled jobs using APScheduler

## API Endpoints

### General
- `GET /` - Welcome message
- `GET /health` - Health check

### Users (Example CRUD)
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get a specific user
- `PUT /api/v1/users/{user_id}` - Update a user
- `DELETE /api/v1/users/{user_id}` - Delete a user

## Development

### Running without Docker
1. Install Python 3.12+
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up PostgreSQL database
5. Update DATABASE_URL in .env
6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Database Migrations
To use Alembic for database migrations:

```bash
# Initialize Alembic (first time only)
docker-compose exec web alembic init alembic

# Create a new migration
docker-compose exec web alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec web alembic upgrade head

# Rollback migration
docker-compose exec web alembic downgrade -1
```

### Stopping the Application
```bash
docker-compose down
```

### Stopping and removing volumes (⚠️ deletes database data)
```bash
docker-compose down -v
```

## Production Deployment

For production, update the Dockerfile CMD to use Gunicorn:

```dockerfile
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "60"]
```

Also update docker-compose.yml command:
```yaml
command: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 60
```

And remember to:
- Set `DEBUG=False` in .env
- Configure CORS properly in `app/main.py`
- Use strong passwords
- Implement proper password hashing (e.g., with `passlib` and `bcrypt`)
- Add authentication and authorization
- Use environment-specific configurations

## Environment Variables

Key environment variables in `.env`:

```env
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=alira_db
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_URL=

APP_NAME=Alira Backend
DEBUG=True
API_V1_PREFIX=/api/v1
```

## Contributing

1. Create a new branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT
