"""
Model Health Cache

Tracks which configured OpenRouter models are currently healthy vs.
temporarily unavailable (rate-limited, overloaded, erroring), and
remembers the last model that successfully served a request so
subsequent requests try it first instead of walking the fallback list
from the top every time.

In-process only (plain dicts, no persistence) -- matching the same
"smallest correct implementation" philosophy as core/broadcaster.py and
scheduler/scheduler.py elsewhere in this codebase. Health state resets
on restart, which is fine: it's inherently short-lived (a model that
was rate-limited five minutes ago is stale information anyway), and
losing it costs nothing worse than the first post-restart request
re-learning it.
"""

from __future__ import annotations

import time

# How long a model that just failed transiently is skipped for before
# being considered a candidate again. Long enough to ride out a typical
# rate-limit window, short enough that a model isn't abandoned for the
# rest of the process's life over one bad request.
_DEFAULT_COOLDOWN_SECONDS = 60


class ModelHealthCache:
    def __init__(self, cooldown_seconds: int = _DEFAULT_COOLDOWN_SECONDS):
        self._cooldown_seconds = cooldown_seconds
        self._unhealthy_until: dict[str, float] = {}
        self._last_healthy_model: str | None = None

    @property
    def last_healthy_model(self) -> str | None:
        return self._last_healthy_model

    def is_healthy(self, model: str) -> bool:
        expiry = self._unhealthy_until.get(model)
        return expiry is None or time.monotonic() >= expiry

    def mark_unhealthy(self, model: str) -> None:
        self._unhealthy_until[model] = time.monotonic() + self._cooldown_seconds

        if self._last_healthy_model == model:
            self._last_healthy_model = None

    def mark_healthy(self, model: str) -> None:
        self._unhealthy_until.pop(model, None)
        self._last_healthy_model = model

    def ordered_candidates(self, configured_models: list[str]) -> list[str]:
        """
        Returns configured_models reordered into the sequence AIService
        should actually try them in:

        1. The last known-healthy model first, if it's still in the
           configured list and isn't itself in a cooldown.
        2. Every other currently-healthy configured model, in the order
           they're configured.
        3. Every currently-unhealthy configured model, in configured
           order, as a last resort -- trying a possibly-since-recovered
           model beats giving up before attempting anything at all.

        Duplicates in the input are preserved as duplicates removed --
        each model is only ever tried once per request regardless of
        how many times it appears in OPENROUTER_MODELS.
        """

        seen: set[str] = set()
        deduped: list[str] = []

        for model in configured_models:
            if model not in seen:
                seen.add(model)
                deduped.append(model)

        healthy = [m for m in deduped if self.is_healthy(m)]
        unhealthy = [m for m in deduped if not self.is_healthy(m)]

        if self._last_healthy_model in healthy:
            healthy.remove(self._last_healthy_model)
            healthy.insert(0, self._last_healthy_model)

        return healthy + unhealthy


model_health = ModelHealthCache()
