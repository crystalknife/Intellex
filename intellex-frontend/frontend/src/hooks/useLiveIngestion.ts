"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";

import { env } from "@/lib/env";
import { logger } from "@/lib/logger";
import { QUERY_KEYS } from "@/lib/constants";

export type LiveConnectionStatus = "connecting" | "open" | "closed";

interface LiveIngestionState {
  connectionStatus: LiveConnectionStatus;
  isSyncing: boolean;
  lastSyncedAt: Date | null;
}

/**
 * Subscribes to the backend's /live/stream SSE endpoint. On every
 * completed ingestion cycle it invalidates the documents/events/pipeline
 * queries so the workspace refreshes with real pushed data instead of
 * waiting on REFETCH_INTERVALS -- those intervals stay in place as a
 * fallback (tab throttling, a dropped connection that hasn't
 * reconnected yet), not as the primary refresh mechanism anymore.
 */
export function useLiveIngestion(): LiveIngestionState {
  const queryClient = useQueryClient();
  const [connectionStatus, setConnectionStatus] =
    useState<LiveConnectionStatus>("connecting");
  const [isSyncing, setIsSyncing] = useState(false);
  const [lastSyncedAt, setLastSyncedAt] = useState<Date | null>(null);

  useEffect(() => {
    const source = new EventSource(`${env.API_URL}/live/stream`);

    setConnectionStatus("connecting");

    source.onopen = () => setConnectionStatus("open");

    source.onerror = () => {
      // EventSource auto-reconnects on its own (per the `retry:` hint
      // the backend sends) -- we just reflect that we're not currently
      // connected while it does.
      setConnectionStatus("closed");
    };

    source.addEventListener("ingestion_started", () => {
      setIsSyncing(true);
    });

    source.addEventListener("ingestion_complete", () => {
      setIsSyncing(false);
      setLastSyncedAt(new Date());

      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.documents() });
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.events() });
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.pipelineStats() });
    });

    source.addEventListener("ingestion_failed", () => {
      setIsSyncing(false);
      logger.warn("Ingestion cycle failed");
    });

    return () => {
      source.close();
    };
  }, [queryClient]);

  return { connectionStatus, isSyncing, lastSyncedAt };
}
