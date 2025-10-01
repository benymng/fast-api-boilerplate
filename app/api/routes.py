from fastapi import APIRouter
from app.users.routes import router as users_router

# Create the main API router
api_router = APIRouter()

# Include all module routers (prefix already defined in users_router)
api_router.include_router(users_router)

# Add more routers here as you create new modules
# api_router.include_router(posts_router, prefix="/posts", tags=["posts"])
# api_router.include_router(comments_router, prefix="/comments", tags=["comments"])
