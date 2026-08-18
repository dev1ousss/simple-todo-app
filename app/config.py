import os
from dataclasses import dataclass


@dataclass
class Settings:
    DATABASE_URL: str
    REDIS_URL: str
    cache_ttl_seconds: int
    cache_tasks_key: str
    cache_categories_key: str
    cors_allowed_origins: list[str]


def get_settings() -> Settings:
    return Settings(
        DATABASE_URL=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://postgres:admin@127.0.0.1:5434/postgres",
        ),
        REDIS_URL=os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
        cache_ttl_seconds=3600,
        cache_tasks_key="cache:tasks_list",
        cache_categories_key="cache:categories_list",
        cors_allowed_origins=["http://localhost:3000"],
    )
