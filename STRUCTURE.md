# Project Structure

This document explains the modular folder structure of the Alira Backend project.

## Directory Structure

```
app/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── config.py               # Application configuration
├── database.py             # Database connection and session management
├── scheduler.py            # Background task scheduler
│
├── api/                    # API route aggregation
│   ├── __init__.py
│   └── routes.py           # Main API router that includes all module routers
│
└── users/                  # Users module (example of domain-based structure)
    ├── __init__.py
    ├── models.py           # User database models
    ├── schemas.py          # User Pydantic schemas (request/response)
    ├── routes.py           # User API endpoints
    └── services.py         # User business logic layer
```

## Module Pattern

Each feature/domain should follow this structure:

```
app/
└── <module_name>/
    ├── __init__.py
    ├── models.py           # SQLAlchemy models
    ├── schemas.py          # Pydantic schemas for validation
    ├── routes.py           # API endpoints (FastAPI routes)
    └── services.py         # Business logic layer
```

### File Responsibilities

#### `models.py`
- Contains SQLAlchemy ORM models
- Defines database table structure
- Relationships between tables
- Example:
  ```python
  from sqlalchemy import Column, Integer, String
  from app.database import Base
  
  class User(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key=True)
      email = Column(String, unique=True)
  ```

#### `schemas.py`
- Pydantic models for request/response validation
- Data transfer objects (DTOs)
- Example:
  ```python
  from pydantic import BaseModel, EmailStr
  
  class UserCreate(BaseModel):
      email: EmailStr
      username: str
  ```

#### `routes.py`
- FastAPI endpoint definitions
- Request handling
- Calls service layer for business logic
- Example:
  ```python
  from fastapi import APIRouter, Depends
  
  router = APIRouter(prefix="/users", tags=["users"])
  
  @router.get("/")
  def get_users():
      return UserService.get_users()
  ```

#### `services.py`
- Business logic layer
- Database operations
- Validation and error handling
- Example:
  ```python
  class UserService:
      @staticmethod
      def get_users(db: Session):
          return db.query(User).all()
  ```

## Adding a New Module

To add a new feature (e.g., `posts`), follow these steps:

1. **Create the module folder structure:**
   ```bash
   mkdir app/posts
   touch app/posts/__init__.py
   touch app/posts/models.py
   touch app/posts/schemas.py
   touch app/posts/routes.py
   touch app/posts/services.py
   ```

2. **Define the model** (`app/posts/models.py`):
   ```python
   from sqlalchemy import Column, Integer, String, ForeignKey
   from app.database import Base
   
   class Post(Base):
       __tablename__ = "posts"
       id = Column(Integer, primary_key=True, index=True)
       title = Column(String, nullable=False)
       content = Column(String)
       user_id = Column(Integer, ForeignKey("users.id"))
   ```

3. **Define schemas** (`app/posts/schemas.py`):
   ```python
   from pydantic import BaseModel
   
   class PostCreate(BaseModel):
       title: str
       content: str
   
   class PostResponse(PostCreate):
       id: int
       user_id: int
       
       class Config:
           from_attributes = True
   ```

4. **Create service layer** (`app/posts/services.py`):
   ```python
   from sqlalchemy.orm import Session
   from app.posts.models import Post
   from app.posts.schemas import PostCreate
   
   class PostService:
       @staticmethod
       def create_post(db: Session, post: PostCreate, user_id: int):
           db_post = Post(**post.model_dump(), user_id=user_id)
           db.add(db_post)
           db.commit()
           db.refresh(db_post)
           return db_post
   ```

5. **Define routes** (`app/posts/routes.py`):
   ```python
   from fastapi import APIRouter, Depends
   from sqlalchemy.orm import Session
   from app.database import get_db
   from app.posts.schemas import PostCreate, PostResponse
   from app.posts.services import PostService
   
   router = APIRouter(prefix="/posts", tags=["posts"])
   
   @router.post("/", response_model=PostResponse)
   def create_post(post: PostCreate, db: Session = Depends(get_db)):
       return PostService.create_post(db, post, user_id=1)
   ```

6. **Register the router** in `app/api/routes.py`:
   ```python
   from app.posts.routes import router as posts_router
   
   api_router.include_router(posts_router)
   ```

## Benefits of This Structure

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Modularity**: Features are isolated and can be developed independently
3. **Testability**: Easy to mock and test individual layers
4. **Scalability**: New features can be added without affecting existing code
5. **Maintainability**: Clear structure makes code easier to navigate and update
6. **Reusability**: Service layer can be reused across different endpoints

## Layer Flow

```
Request → Route → Service → Model → Database
                    ↓
Response ← Route ← Service ← Model ← Database
```

1. **Route Layer**: Handles HTTP requests/responses
2. **Service Layer**: Contains business logic
3. **Model Layer**: Database operations via ORM
4. **Database**: PostgreSQL storage

## Example: User Module

The `users` module demonstrates this pattern:

- `models.py`: User SQLAlchemy model
- `schemas.py`: UserCreate, UserUpdate, UserResponse schemas
- `services.py`: UserService with CRUD operations
- `routes.py`: User API endpoints

All user routes are automatically included under `/api/v1/users/` through the API router.
