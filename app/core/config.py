from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LOV Portal API"
    api_prefix: str = ""

    # BigQuery
    bigquery_project: str = "your-project-id"
    bigquery_dataset: str = "lov_gold"
    bigquery_location: str = "asia-southeast2"
    google_application_credentials: str | None = None

    # Redis (cache, dipake khusus router v1 /lov/v1/company/*) - no Postgres
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None
    cache_ttl_seconds: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
