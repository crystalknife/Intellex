"""
OpenRouter Client

Thin wrapper around the OpenAI SDK pointed at OpenRouter's OpenAI-
compatible endpoint. Lazily constructed so importing this module never
fails even when no API key is configured -- the error only surfaces
when something actually tries to call the model.
"""

from openai import AsyncOpenAI

from backend.app.config import settings


class AINotConfiguredError(Exception):
    """Raised when an AI endpoint is called without OPENROUTER_API_KEY set."""


_client: AsyncOpenAI | None = None


def is_configured() -> bool:
    return bool(settings.OPENROUTER_API_KEY.strip())


def get_client() -> AsyncOpenAI:
    global _client

    if not is_configured():
        raise AINotConfiguredError(
            "OPENROUTER_API_KEY is not set. Add it to backend/.env to "
            "enable AI Workspace."
        )

    if _client is None:
        _client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
        )

    return _client
