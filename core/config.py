from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DB_NAME: SecretStr = Field("travel", env="DB_NAME")
    DB_USER: SecretStr = Field(default="travel", env="DB_USER")
    DB_PASSWORD: SecretStr = Field("password", env="DB_PASSWORD")
    DB_HOST: str = Field("localhost", env="HOST")
    DB_PORT: int = Field(5432, env="PORT")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    db: DatabaseSettings = DatabaseSettings()
    SECRET_KEY: SecretStr
    CORS_ALLOWED_ORIGINS: str
    DEBUG: bool


settings = Settings()

print(settings.model_dump())
