from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LOV Portal API"
    api_prefix: str = ""

    # BigQuery
    bigquery_project: str = "your-project-id"
    bigquery_dataset: str = "lov_gold"
    bigquery_location: str = "asia-southeast2"
    google_application_credentials: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
