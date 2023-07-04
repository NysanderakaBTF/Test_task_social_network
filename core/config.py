import os

from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    DB_URL: PostgresDsn
    JWT_SECRET_KEY: str = f"{os.getenv('JWT_SECRET_KEY')}"
    JWT_ALGORITHM: str = f"{os.getenv('JWT_ALGORITHM')}"

config = Config()
