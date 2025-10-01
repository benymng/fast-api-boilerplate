from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Alira Backend"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"  # development, production

    # Local Database
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_NAME: str = "alira_db"
    DATABASE_HOST: str = "postgres"
    DATABASE_PORT: str = "5432"
    DATABASE_URL: str = ""

    # Production Database (Supabase)
    PROD_DATABASE_URL: str = ""
    PROD_DATABASE_USER: str = ""
    PROD_DATABASE_PASSWORD: str = ""
    PROD_DATABASE_NAME: str = "postgres"
    PROD_DATABASE_HOST: str = ""
    PROD_DATABASE_PORT: str = "6543"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_database_url(self) -> str:
        """Get the appropriate database URL based on environment"""
        if self.ENVIRONMENT == "production":
            # Use PROD_DATABASE_URL if provided, otherwise construct it
            if self.PROD_DATABASE_URL:
                return self.PROD_DATABASE_URL
            return f"postgresql://{self.PROD_DATABASE_USER}:{self.PROD_DATABASE_PASSWORD}@{self.PROD_DATABASE_HOST}:{self.PROD_DATABASE_PORT}/{self.PROD_DATABASE_NAME}"
        else:
            # Use local database (for development with Docker)
            if self.DATABASE_URL:
                return self.DATABASE_URL
            return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
