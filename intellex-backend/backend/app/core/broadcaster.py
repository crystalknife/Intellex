"""
Live Event Broadcaster

A minimal in-process asyncio pub/sub used to push ingestion-cycle events
to connected SSE clients (see api/routers/live.py). Deliberately the
smallest correct implementation, matching the same philosophy as
scheduler.py: no Redis, no message broker, just asyncio primitives.

Single-process only -- correct for the current SQLite/single-worker
deployment model. If Intellex ever runs multiple worker processes, this
needs to move to a shared backend (Redis pub/sub, etc.) since
asyncio.Queue only broadcasts within one process's memory.
"""

from __future__ import annotations

import asyncio
from typing import Any


class LiveBroadcaster:
    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue] = set()

    def subscribe(self) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=32)
        self._subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue) -> None:
        self._subscribers.discard(queue)

    async def publish(self, event_type: str, payload: dict[str, Any]) -> None:
        """
        Fan out an event to every connected subscriber. A slow/stalled
        subscriber whose queue is full is dropped rather than allowed to
        block ingestion for everyone else -- it'll pick up fresh state on
        its next reconnect anyway, via the normal query invalidation.
        """

        dead: list[asyncio.Queue] = []

        for queue in self._subscribers:
            try:
                queue.put_nowait({"type": event_type, "payload": payload})
            except asyncio.QueueFull:
                dead.append(queue)

        for queue in dead:
            self._subscribers.discard(queue)


broadcaster = LiveBroadcaster()
