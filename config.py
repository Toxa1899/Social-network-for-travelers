from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )
    DB_NAME: SecretStr
    DB_USER: SecretStr
    DB_PASSWORD: SecretStr
    HOST: str
    PORT: int
    SECRET_KEY: SecretStr


settings = DatabaseSettings()
