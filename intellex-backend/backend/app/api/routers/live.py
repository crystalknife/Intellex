"""
Live Router

Server-Sent Events endpoint that pushes ingestion-cycle events
(started / complete / failed) to connected clients, so the frontend can
invalidate its document/event/pipeline queries the moment new data
lands instead of waiting on a blind poll interval.

SSE over WebSockets was a deliberate choice: this is one-directional
(server -> client) only, it needs no new dependency (plain
StreamingResponse), and the browser's native EventSource already
handles reconnect/backoff for us.

Auth: the native EventSource API cannot set an Authorization header, so
unlike every other protected route this one accepts the access token as
a `token` query parameter instead of a bearer header. The token is
decoded and validated exactly the same way (same JWT, same secret) --
this is a transport-level accommodation, not a weaker auth scheme.
"""

import asyncio
import json

from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import StreamingResponse

from backend.app.core.broadcaster import broadcaster
from backend.app.core.logger import get_logger
from backend.app.core.security import InvalidTokenError, decode_access_token

logger = get_logger("LiveRouter")

router = APIRouter(
    prefix="/live",
    tags=["Live"],
)

_HEARTBEAT_SECONDS = 20


@router.get("/stream")
async def stream(request: Request, token: str = Query(...)):
    try:
        payload = decode_access_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    organization_id = payload["org_id"]
    queue = broadcaster.subscribe(organization_id)

    async def event_generator():
        try:
            # Tell EventSource how long to wait before auto-reconnecting
            # if the connection drops.
            yield "retry: 3000\n\n"

            while True:
                if await request.is_disconnected():
                    break

                try:
                    event = await asyncio.wait_for(
                        queue.get(), timeout=_HEARTBEAT_SECONDS
                    )
                    yield (
                        f"event: {event['type']}\n"
                        f"data: {json.dumps(event['payload'])}\n\n"
                    )
                except asyncio.TimeoutError:
                    # Comment-only line -- keeps proxies/load balancers
                    # from timing out an idle connection. Not a real
                    # event, EventSource ignores it.
                    yield ": heartbeat\n\n"
        finally:
            broadcaster.unsubscribe(organization_id, queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # Disable response buffering on nginx-style proxies so
            # events actually stream instead of batching.
            "X-Accel-Buffering": "no",
        },
    )
