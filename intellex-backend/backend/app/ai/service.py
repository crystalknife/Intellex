"""
AI Service
...
"""

import re
from typing import Literal, TypedDict

from sqlalchemy.orm import Session

from backend.app.ai.client import AINotConfiguredError, get_client, is_configured
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


# --- rest of file unchanged above this point --------------------------

class AIRequestError(Exception):
    """Raised when the upstream OpenRouter call itself fails."""


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

        repo = DocumentRepository(db)

        results, _ = repo.search(question, organization_id, limit=_MAX_CONTEXT_DOCS)

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

        sources: list[AISource] = [
            {
                "id": doc.id,
                "title": doc.title,
                "url": doc.url,
                "source": doc.source,
            }
            for doc in results
        ]

        return {
            "answer": answer,
            "sources": sources,
            "model": settings.OPENROUTER_MODEL,
        }