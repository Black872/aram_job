from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ARAM API"
    app_env: str = "development"
    app_secret_key: str = "development-only-change-me"
    database_url: str = "postgresql+psycopg://aram:aram@localhost:5432/aram"
    gmail_label_name: str = "Job Applications"
    automation_mode: str = "assisted"
    dry_run: bool = True
    ai_confidence_threshold: float = 0.90

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
