import os
from dataclasses import dataclass


@dataclass
class Settings:
    DATABASE_URL: str
    cors_allowed_origins: list[str]


def get_settings() -> Settings:
    return Settings(
        DATABASE_URL=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://postgres:admin@127.0.0.1:5434/postgres",
        ),
        cors_allowed_origins=["http://localhost:3000"],
    )
