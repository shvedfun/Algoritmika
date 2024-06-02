import os
import secrets
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = f"Algoritmika"
    DESCRIPTION: str = "For Algoritmika"
    ENV: Literal["development", "staging", "production"] = "development"
    VERSION: str = "0.2"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/algoritmika"
    API_USERNAME: str = os.getenv('USERNAME', '') #"svc_test"
    API_PASSWORD: str = os.getenv('PASSWORD', '') #"superstrongpassword"

    class Config:
        case_sensitive = True


settings = Settings()


class TestSettings(Settings):
    class Config:
        case_sensitive = True


test_settings = TestSettings()
