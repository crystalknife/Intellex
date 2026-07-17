# AI Workspace: Model Fallback

## What changed

AI Workspace previously called a single hardcoded OpenRouter model
(`OPENROUTER_MODEL`). Free-tier models get rate-limited (HTTP 429) or
go temporarily unavailable, and a single-model setup had no way to
recover from that within a request -- it just failed.

Model selection is now entirely configuration-driven and supports
automatic failover across an ordered list of models.

## Configuration

`backend/.env`:

```
OPENROUTER_MODELS=google/gemma-4-31b-it:free,openrouter/free
```

- Comma-separated, ordered. Whitespace around entries is trimmed.
- Not a single model -- a fallback *list*. There is no hardcoded model
  name anywhere in the codebase; this variable is the only source of
  truth for which models are used and in what order.
- Check <https://openrouter.ai/models?max_price=0> for currently
  available free models -- free-tier availability rotates, so treat
  the shipped default as a starting point, not a guarantee.
- `openrouter/free` (OpenRouter's own free-model auto-router) is a
  reasonable last entry in any list, since it's documented as a
  permanent, stable option that itself spreads load across whichever
  free models are currently healthy on OpenRouter's side.

## How the fallback works

Implemented in `backend/app/ai/service.py` (`AIService.answer_question`)
and `backend/app/ai/model_health.py` (`ModelHealthCache`).

On every request:

1. Build the ordered list of candidate models: the last model that
   successfully served a request goes first (if it's still configured
   and not currently in cooldown), then the rest of the configured
   models that are currently healthy, then any configured models
   currently in cooldown, as a last resort.
2. Try the first candidate. If it succeeds, use its answer, remember it
   as the healthy model for next time, and log which model served the
   request.
3. If it fails with a **transient** error -- HTTP 429, timeout,
   connection error, or a 5xx/provider-overloaded response -- mark that
   model unhealthy for 60 seconds and try the next candidate.
4. If it fails with a **non-transient** error (bad API key, malformed
   request) -- fail immediately rather than cycling through every
   remaining model, since a different model won't fix an auth problem.
5. If every configured model fails, the request fails with a single
   clean, generic message: *"AI Workspace is temporarily unavailable --
   every configured model failed to respond. Please try again in a
   moment."* Full failure details for every attempted model are logged
   server-side; the person asking the question never sees raw
   provider/HTTP error text.

Health state is in-memory only (no database, no Redis) -- consistent
with the rest of this codebase's "smallest correct implementation"
approach (see `core/broadcaster.py`, `scheduler/scheduler.py`). It
resets on backend restart, which costs nothing worse than the first
post-restart request re-learning which models are currently healthy.

## Observability

- `GET /ai/status` reports the first configured model as a
  representative "primary" model for display purposes.
- Every `POST /ai/chat` response's `model` field reports the model that
  *actually* served that specific response -- which can differ from
  request to request if fallback occurred.
- Every model attempt (success, transient failure, non-transient
  failure, and total exhaustion) is logged via the existing structured
  logger under the `AIService` name.
