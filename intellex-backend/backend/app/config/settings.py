"""
Application Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Defaults to a local SQLite file so the app runs with zero config in
    # development. Override with a Postgres DSN (e.g.
    # postgresql+psycopg://user:pass@localhost:5432/intellex) in production.
    DATABASE_URL: str = "sqlite:///./intellex.db"

    # Comma-separated list of allowed browser origins for CORS.
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # How often the background ingestion cycle re-collects + re-processes
    # every configured feed, in minutes.
    REFRESH_INTERVAL_MINUTES: int = 15

    # Whether to kick off an ingestion cycle immediately on startup instead
    # of waiting for the first interval to elapse.
    RUN_INGESTION_ON_STARTUP: bool = True

    # Minimum shared-keyword overlap for two documents to be clustered into
    # the same event by EventBuilder.
    EVENT_KEYWORD_OVERLAP_THRESHOLD: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


settings = Settings()