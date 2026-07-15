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
"""

import asyncio
import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from backend.app.core.broadcaster import broadcaster
from backend.app.core.logger import get_logger

logger = get_logger("LiveRouter")

router = APIRouter(
    prefix="/live",
    tags=["Live"],
)

_HEARTBEAT_SECONDS = 20


@router.get("/stream")
async def stream(request: Request):
    queue = broadcaster.subscribe()

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
            broadcaster.unsubscribe(queue)

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
