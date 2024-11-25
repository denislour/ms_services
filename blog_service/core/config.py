from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/blog_db"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Blog Service"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
