"""
AI Service
<<<<<<< HEAD
...
=======

Answers questions about the current document corpus using OpenRouter.
Retrieval here is keyword/full-text search against the existing
document store (DocumentRepository.search, falling back to the most
recent documents if nothing matches) -- not vector-embedding based.
That's a deliberately honest scope: it's genuinely retrieval-augmented
generation, just without an embeddings index, which keeps this feature
usable on a $0 OpenRouter key with no extra infrastructure (no vector
DB, no embedding model/cost).

Model selection is entirely configuration-driven (OPENROUTER_MODELS in
.env, an ordered comma-separated fallback list -- see
config/settings.py) with automatic failover: if a model is rate-limited,
times out, or its provider is overloaded/unavailable, the next
configured model is tried instead of failing the request outright. See
model_health.py for the health-tracking/cooldown bookkeeping this relies
on.
>>>>>>> 76704d7 (feat: add AI workspace, authentication, collections, and platform infrastructure)
"""

import re
from typing import Literal, TypedDict

<<<<<<< HEAD
from sqlalchemy.orm import Session

from backend.app.ai.client import AINotConfiguredError, get_client, is_configured
=======
import openai
from sqlalchemy.orm import Session

from backend.app.ai.client import AINotConfiguredError, get_client, is_configured
from backend.app.ai.model_health import model_health
>>>>>>> 76704d7 (feat: add AI workspace, authentication, collections, and platform infrastructure)
from backend.app.config import settings
from backend.app.core.logger import get_logger
from backend.app.repositories.document_repository import DocumentRepository

logger = get_logger("AIService")

# --- reasoning-leak guards -------------------------------------------------
# Some OpenRouter providers for reasoning models (e.g. openai/gpt-oss-*)
# don't cleanly separate chain-of-thought from the final answer even when
# `reasoning.exclude` is requested. These patterns catch the common leak
# shapes (raw <think> blocks, and OpenAI's harmony analysis/final channel
# markers) so internal deliberation never reaches the user.
_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_HARMONY_FINAL_RE = re.compile(
    r"<\|channel\|>final<\|message\|>|assistantfinal", re.IGNORECASE
)


def _strip_reasoning(raw: str) -> str:
    text = _THINK_BLOCK_RE.sub("", raw)
    match = _HARMONY_FINAL_RE.search(text)
    if match:
        text = text[match.end():]
    return text.strip()


<<<<<<< HEAD
# --- rest of file unchanged above this point --------------------------

class AIRequestError(Exception):
    """Raised when the upstream OpenRouter call itself fails."""
=======
# --- model fallback classification -----------------------------------------

# Exceptions that mean "this specific model/provider is temporarily
# unavailable" -- worth marking the model unhealthy and retrying the
# next configured one. Deliberately narrower than "catch everything":
# an auth or bad-request error means retrying a *different* model won't
# help either (a bad API key fails identically for every model), so
# those propagate immediately instead of silently burning through the
# whole fallback list first.
_TRANSIENT_EXCEPTION_TYPES = (
    openai.RateLimitError,
    openai.APITimeoutError,
    openai.APIConnectionError,
    openai.InternalServerError,
)

# Some transient failures (provider overload, "no instances available")
# surface as a generic APIStatusError rather than one of the specific
# classes above -- catch those by HTTP status code instead.
_TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


def _is_transient(error: Exception) -> bool:
    if isinstance(error, _TRANSIENT_EXCEPTION_TYPES):
        return True

    return getattr(error, "status_code", None) in _TRANSIENT_STATUS_CODES


class AIRequestError(Exception):
    """Raised when every configured model fails to answer the request."""
>>>>>>> 76704d7 (feat: add AI workspace, authentication, collections, and platform infrastructure)


class ChatTurn(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class AISource(TypedDict):
    id: str
    title: str
    url: str
    source: str


class AIAnswer(TypedDict):
    answer: str
    sources: list[AISource]
    model: str


_MAX_CONTEXT_DOCS = 8
_MAX_SNIPPET_CHARS = 600

_SYSTEM_PROMPT_TEMPLATE = (
    "You are Intellex, a news intelligence assistant. Answer the "
    "user's question using ONLY the numbered articles below as your "
    "source of truth. Cite articles inline like [1] or [2] when you "
    "reference a specific claim. If the articles don't contain enough "
    "information to answer confidently, say so directly instead of "
    "guessing or relying on outside knowledge.\n\nARTICLES:\n{context}"
)


class AIService:

    @staticmethod
    async def answer_question(
        question: str,
        history: list[ChatTurn],
        db: Session,
        organization_id: str,
    ) -> AIAnswer:

        if not is_configured():
            raise AINotConfiguredError()

<<<<<<< HEAD
        repo = DocumentRepository(db)

        results, _ = repo.search(question, organization_id, limit=_MAX_CONTEXT_DOCS)
=======
        configured_models = settings.openrouter_models_list

        if not configured_models:
            logger.error("OPENROUTER_MODELS is empty -- no models configured")
            raise AIRequestError(
                "AI Workspace is misconfigured (no models set). Please "
                "contact your administrator."
            )

        repo = DocumentRepository(db)

        results, _ = repo.search(
            question, organization_id, limit=_MAX_CONTEXT_DOCS
        )
>>>>>>> 76704d7 (feat: add AI workspace, authentication, collections, and platform infrastructure)

        if not results:
            results, _ = repo.list_documents(
                organization_id, limit=_MAX_CONTEXT_DOCS
            )

        context_blocks = []

        for i, doc in enumerate(results, start=1):
            snippet = (doc.summary or doc.content or "")[:_MAX_SNIPPET_CHARS]
            context_blocks.append(
                f"[{i}] {doc.title} ({doc.source})\n{snippet}"
            )

        context_text = (
            "\n\n".join(context_blocks)
            if context_blocks
            else "No articles are currently available in the corpus."
        )

        messages = [
            {
                "role": "system",
                "content": _SYSTEM_PROMPT_TEMPLATE.format(context=context_text),
            }
        ]

        for turn in history[-6:]:
            messages.append({"role": turn["role"], "content": turn["content"]})

        messages.append({"role": "user", "content": question})

<<<<<<< HEAD
        client = get_client()

        try:
            response = await client.chat.completions.create(
                model=settings.OPENROUTER_MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=800,
                extra_body={"reasoning": {"exclude": True}},
            )
        except Exception as e:
            logger.error(f"OpenRouter request failed: {e}")
            raise AIRequestError(str(e)) from e

        raw_answer = response.choices[0].message.content or ""
        answer = _strip_reasoning(raw_answer)

=======
>>>>>>> 76704d7 (feat: add AI workspace, authentication, collections, and platform infrastructure)
        sources: list[AISource] = [
            {
                "id": doc.id,
                "title": doc.title,
                "url": doc.url,
                "source": doc.source,
            }
            for doc in results
        ]

<<<<<<< HEAD
        return {
            "answer": answer,
            "sources": sources,
            "model": settings.OPENROUTER_MODEL,
        }
=======
        client = get_client()
        candidates = model_health.ordered_candidates(configured_models)
        last_error: Exception | None = None

        for model in candidates:
            try:
                response = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=800,
                    extra_body={"reasoning": {"exclude": True}},
                )
            except Exception as e:
                last_error = e

                if _is_transient(e):
                    model_health.mark_unhealthy(model)
                    logger.warning(
                        f"AI model '{model}' failed transiently "
                        f"({type(e).__name__}: {e}) -- falling back to "
                        f"next configured model"
                    )
                    continue

                # Non-transient (bad API key, malformed request, etc.)
                # -- a different model won't fix this, so fail fast
                # rather than cycling through the rest of the list.
                logger.error(
                    f"AI model '{model}' failed non-transiently, "
                    f"aborting fallback: {type(e).__name__}: {e}"
                )
                raise AIRequestError(
                    "The AI request failed. Please try again shortly."
                ) from e

            model_health.mark_healthy(model)
            logger.info(f"AI request served by model={model}")

            raw_answer = response.choices[0].message.content or ""
            answer = _strip_reasoning(raw_answer)

            return {
                "answer": answer,
                "sources": sources,
                "model": model,
            }

        logger.error(
            f"All {len(candidates)} configured AI model(s) failed for "
            f"this request. Last error: {last_error}"
        )
        raise AIRequestError(
            "AI Workspace is temporarily unavailable -- every configured "
            "model failed to respond. Please try again in a moment."
        )
>>>>>>> 76704d7 (feat: add AI workspace, authentication, collections, and platform infrastructure)
