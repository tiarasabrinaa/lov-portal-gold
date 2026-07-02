from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LOV Portal API"
    api_prefix: str = ""
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/lov_portal"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
