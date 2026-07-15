"""
Application Settings
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# settings.py -> config -> app -> backend  (where .env actually lives)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


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

    # AI Workspace (optional). Empty by default -- the /ai endpoints report
    # themselves as unconfigured rather than erroring when this is unset,
    # so the rest of the app works fine without an API key.
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "google/gemma-4-31b-it:free"

    # Auth. JWT_SECRET has a dev-only fallback so the app still runs with
    # zero config locally, matching the rest of this file's philosophy --
    # but it MUST be overridden via .env with a long random value before
    # this is ever exposed outside localhost, since anyone who knows the
    # default can forge tokens.
    JWT_SECRET: str = "dev-only-insecure-secret-override-in-env"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
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