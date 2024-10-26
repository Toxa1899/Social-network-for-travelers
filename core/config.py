from typing import ClassVar

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DB_NAME: SecretStr = Field("prediction", env="DB_NAME")
    DB_USER: SecretStr = Field(default="prediction", env="DB_USER")
    DB_PASSWORD: SecretStr = Field("prediction", env="DB_PASSWORD")
    DB_HOST: str = Field("postgres-db", env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    db: DatabaseSettings = DatabaseSettings()
    SECRET_KEY: SecretStr = Field("change_me", env="SECRET_KEY")
    CORS_ALLOWED_ORIGINS: str = Field(
        "http://localhost:3000", env="CORS_ALLOWED_ORIGINS"
    )
    DEBUG: bool = Field(True, env="DEBUG")
    JWT_SECRET_KEY: SecretStr = Field("JWT_SECRET_KEY", env="JWT_SECRET_KEY")
    ACCESS_KEY: SecretStr = Field(
        "1d10f82dd4a2cc5b16a2f70590d3c3a9", env="ACCESS_KEY"
    )
    ALLOWED_HOSTS: SecretStr = Field("*", env="ALLOWED_HOSTS")
    CELERY_BROKER_URL: str = Field(
        "redis://127.0.0.1:6379/0", env="CELERY_BROKER_URL"
    )
    CELERY_BROKER_TRANSPORT: str = Field(
        "redis", env="CELERY_BROKER_TRANSPORT"
    )

    CELERY_RESULT_BACKEND: str = Field(
        "redis://redis:6379/0", env="CELERY_RESULT_BACKEND"
    )

    MEGABYTE_LIMIT: int = Field(5, env="MEGABYTE_LIMIT")


settings = Settings()
