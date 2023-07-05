import os

from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    DB_URL: str = f"{os.getenv('DB_URL')}"
    JWT_SECRET_KEY: str = f"{os.getenv('JWT_SECRET_KEY')}"
    JWT_ALGORITHM: str = f"{os.getenv('JWT_ALGORITHM')}"
    EMAIL_HUNTER_API_KEY: str = f"{os.getenv('EMAIL_HUNTER_API_KEY')}"


config = Config()
