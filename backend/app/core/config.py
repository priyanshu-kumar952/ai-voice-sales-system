from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Voice AI Sales System"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    database_url: str = ""
    webhook_secret: str = ""
    n8n_webhook_url: str = ""
    n8n_webhook_secret: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()









