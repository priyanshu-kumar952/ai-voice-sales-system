from psycopg_pool import ConnectionPool
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    database_url: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


database_settings = DatabaseSettings()

pool = ConnectionPool(
    conninfo=database_settings.database_url,
    min_size=1,
    max_size=10,
)