"""
AI model fallback tests.

Covers ModelHealthCache in isolation and AIService.answer_question's
retry loop against realistic mocked OpenAI SDK exceptions (real
httpx.Request/Response objects, not just bare strings) -- these are the
same scenarios that were verified by hand while building the fallback
system, formalized into a repeatable suite.
"""

import httpx
import openai
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.app.ai.model_health import ModelHealthCache


# --- ModelHealthCache unit tests -------------------------------------------


def test_fresh_cache_preserves_configured_order():
    cache = ModelHealthCache(cooldown_seconds=60)
    assert cache.ordered_candidates(["a", "b", "c"]) == ["a", "b", "c"]


def test_unhealthy_model_is_pushed_to_the_end():
    cache = ModelHealthCache(cooldown_seconds=60)
    cache.mark_unhealthy("a")
    assert cache.ordered_candidates(["a", "b", "c"]) == ["b", "c", "a"]


def test_last_healthy_model_is_tried_first():
    cache = ModelHealthCache(cooldown_seconds=60)
    cache.mark_unhealthy("a")
    cache.mark_healthy("b")
    assert cache.last_healthy_model == "b"
    assert cache.ordered_candidates(["a", "b", "c"]) == ["b", "c", "a"]


def test_marking_healthy_clears_cooldown():
    cache = ModelHealthCache(cooldown_seconds=60)
    cache.mark_unhealthy("a")
    cache.mark_healthy("a")
    assert cache.is_healthy("a") is True
    assert cache.ordered_candidates(["a", "b", "c"]) == ["a", "b", "c"]


def test_duplicate_configured_models_are_deduplicated():
    cache = ModelHealthCache()
    assert cache.ordered_candidates(["x", "x", "y"]) == ["x", "y"]


# --- AIService fallback integration tests ----------------------------------


def _rate_limit_error() -> openai.RateLimitError:
    request = httpx.Request("POST", "https://openrouter.ai/api/v1/chat/completions")
    response = httpx.Response(429, request=request, json={"error": {"message": "rate limited"}})
    return openai.RateLimitError("rate limited", response=response, body=None)


def _auth_error() -> openai.AuthenticationError:
    request = httpx.Request("POST", "https://openrouter.ai/api/v1/chat/completions")
    response = httpx.Response(401, request=request, json={"error": {"message": "bad key"}})
    return openai.AuthenticationError("bad key", response=response, body=None)


def _success_response(content: str = "Test answer [1]") -> MagicMock:
    message = MagicMock()
    message.content = content
    choice = MagicMock()
    choice.message = message
    response = MagicMock()
    response.choices = [choice]
    return response


@pytest.fixture(autouse=True)
def _reset_model_health():
    """Every test gets a clean model-health cache, not shared global state."""

    import backend.app.ai.model_health as model_health_module
    import backend.app.ai.service as service_module

    fresh = model_health_module.ModelHealthCache()
    model_health_module.model_health = fresh
    service_module.model_health = fresh
    yield


@pytest.mark.asyncio
async def test_falls_back_to_next_model_on_rate_limit(client, signed_up_org):
    from backend.app.ai.service import AIService
    from backend.app.db.session import SessionLocal

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[_rate_limit_error(), _success_response("Fell back OK")]
    )

    db = SessionLocal()
    try:
        with patch("backend.app.ai.service.get_client", return_value=mock_client), patch(
            "backend.app.ai.service.is_configured", return_value=True
        ):
            result = await AIService.answer_question(
                "test question", [], db, signed_up_org["org_id"]
            )
    finally:
        db.close()

    assert result["model"] == "test-model-b:free"
    assert "Fell back OK" in result["answer"]
    assert mock_client.chat.completions.create.call_count == 2


@pytest.mark.asyncio
async def test_cached_healthy_model_is_tried_first_next_time(client, signed_up_org):
    from backend.app.ai.service import AIService
    from backend.app.db.session import SessionLocal

    db = SessionLocal()
    try:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            side_effect=[_rate_limit_error(), _success_response("first")]
        )
        with patch("backend.app.ai.service.get_client", return_value=mock_client), patch(
            "backend.app.ai.service.is_configured", return_value=True
        ):
            await AIService.answer_question("q1", [], db, signed_up_org["org_id"])

        mock_client2 = MagicMock()
        mock_client2.chat.completions.create = AsyncMock(
            side_effect=[_success_response("second")]
        )
        with patch("backend.app.ai.service.get_client", return_value=mock_client2), patch(
            "backend.app.ai.service.is_configured", return_value=True
        ):
            result2 = await AIService.answer_question("q2", [], db, signed_up_org["org_id"])
    finally:
        db.close()

    assert result2["model"] == "test-model-b:free"
    assert mock_client2.chat.completions.create.call_count == 1


@pytest.mark.asyncio
async def test_all_models_failing_raises_clean_error(client, signed_up_org):
    from backend.app.ai.service import AIService, AIRequestError
    from backend.app.db.session import SessionLocal

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[_rate_limit_error(), _rate_limit_error()]
    )

    db = SessionLocal()
    try:
        with patch("backend.app.ai.service.get_client", return_value=mock_client), patch(
            "backend.app.ai.service.is_configured", return_value=True
        ):
            with pytest.raises(AIRequestError) as exc_info:
                await AIService.answer_question("test", [], db, signed_up_org["org_id"])
    finally:
        db.close()

    assert "try again" in str(exc_info.value).lower()
    assert "rate limited" not in str(exc_info.value).lower()
    assert mock_client.chat.completions.create.call_count == 2


@pytest.mark.asyncio
async def test_non_transient_error_aborts_without_trying_other_models(client, signed_up_org):
    from backend.app.ai.service import AIService, AIRequestError
    from backend.app.db.session import SessionLocal

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(side_effect=[_auth_error()])

    db = SessionLocal()
    try:
        with patch("backend.app.ai.service.get_client", return_value=mock_client), patch(
            "backend.app.ai.service.is_configured", return_value=True
        ):
            with pytest.raises(AIRequestError):
                await AIService.answer_question("test", [], db, signed_up_org["org_id"])
    finally:
        db.close()

    assert mock_client.chat.completions.create.call_count == 1


def test_ai_status_reports_primary_configured_model(client):
    response = client.get("/ai/status")
    assert response.status_code == 200
    body = response.json()
    assert body["configured"] is True
    assert body["model"] == "test-model-a:free"


def test_ai_chat_requires_auth(client):
    response = client.post("/ai/chat", json={"question": "test", "history": []})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_ai_chat_over_http_reports_actual_serving_model(client, signed_up_org):
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[_rate_limit_error(), _success_response("Via HTTP")]
    )

    with patch("backend.app.ai.service.get_client", return_value=mock_client):
        response = client.post(
            "/ai/chat",
            json={"question": "test", "history": []},
            headers=signed_up_org["headers"],
        )

    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "test-model-b:free"
    assert "Via HTTP" in body["answer"]
