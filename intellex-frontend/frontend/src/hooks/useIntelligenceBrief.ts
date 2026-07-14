"use client";

import { useMemo } from "react";

import { useDocuments } from "@/hooks/useDocuments";
import { useEvents } from "@/hooks/useEvents";
import { usePipelineStats } from "@/hooks/usePipelineStats";
import { deriveIntelligenceBrief } from "@/services/intelligence.service";

/**
 * Stable interface for the AI Intelligence Brief. Today it derives text
 * client-side from a recent document/event sample plus the true
 * pipeline totals (no extra request beyond what the workspace already
 * fetches). When a real LLM-backed /ai/brief endpoint exists, this hook
 * switches to useQuery(getIntelligenceBrief) and every consumer stays
 * unchanged.
 */
export function useIntelligenceBrief() {
  const documentsQuery = useDocuments({ limit: 100 });
  const eventsQuery = useEvents({ limit: 100 });
  const statsQuery = usePipelineStats();

  const brief = useMemo(() => {
    if (!documentsQuery.data || !eventsQuery.data || !statsQuery.data) {
      return null;
    }

    return deriveIntelligenceBrief(
      documentsQuery.data.items,
      eventsQuery.data.items,
      {
        totalDocuments: statsQuery.data.totalDocuments,
        totalEvents: statsQuery.data.totalEvents,
        totalSources: statsQuery.data.totalSources,
      }
    );
  }, [documentsQuery.data, eventsQuery.data, statsQuery.data]);

  return {
    data: brief,
    isLoading:
      documentsQuery.isLoading || eventsQuery.isLoading || statsQuery.isLoading,
    isError: documentsQuery.isError || eventsQuery.isError || statsQuery.isError,
  };
}
