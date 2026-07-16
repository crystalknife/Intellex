"""
Live Event Broadcaster

A minimal in-process asyncio pub/sub used to push ingestion-cycle events
to connected SSE clients (see api/routers/live.py). Deliberately the
smallest correct implementation, matching the same philosophy as
scheduler.py: no Redis, no message broker, just asyncio primitives.

Organization-scoped: every subscription and publish is keyed by
organization_id, so org A's browser tab never receives a push event
about org B's ingestion cycle. This mirrors the same private-per-org
boundary as the rest of Phase B.

Single-process only -- correct for the current SQLite/single-worker
deployment model. If Intellex ever runs multiple worker processes, this
needs to move to a shared backend (Redis pub/sub, etc.) since
asyncio.Queue only broadcasts within one process's memory.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any


class LiveBroadcaster:
    def __init__(self) -> None:
        self._subscribers: dict[str, set[asyncio.Queue]] = defaultdict(set)

    def subscribe(self, organization_id: str) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=32)
        self._subscribers[organization_id].add(queue)
        return queue

    def unsubscribe(self, organization_id: str, queue: asyncio.Queue) -> None:
        self._subscribers[organization_id].discard(queue)

        if not self._subscribers[organization_id]:
            del self._subscribers[organization_id]

    async def publish(
        self, organization_id: str, event_type: str, payload: dict[str, Any]
    ) -> None:
        """
        Fan out an event to every subscriber connected for this specific
        organization. A slow/stalled subscriber whose queue is full is
        dropped rather than allowed to block ingestion for everyone else
        -- it'll pick up fresh state on its next reconnect anyway, via
        the normal query invalidation.
        """

        subscribers = self._subscribers.get(organization_id)

        if not subscribers:
            return

        dead: list[asyncio.Queue] = []

        for queue in subscribers:
            try:
                queue.put_nowait({"type": event_type, "payload": payload})
            except asyncio.QueueFull:
                dead.append(queue)

        for queue in dead:
            subscribers.discard(queue)


broadcaster = LiveBroadcaster()
