import { apiClient } from "@/lib/api/client";
import type { PipelineStats } from "@/lib/types";

interface RawPipelineStats {
  total_documents: number;
  total_events: number;
  total_sources: number;
  sources: string[];
  last_run_at: string | null;
  last_run_fetched: number;
  last_run_unique: number;
  dedup_rate: number;
  refresh_interval_minutes: number;
  is_running: boolean;
}

export async function getPipelineStats(): Promise<PipelineStats> {
  const { data } = await apiClient.get<RawPipelineStats>(
    "/analytics/pipeline"
  );

  return {
    totalDocuments: data.total_documents,
    totalEvents: data.total_events,
    totalSources: data.total_sources,
    sources: data.sources,
    lastRunAt: data.last_run_at,
    lastRunFetched: data.last_run_fetched,
    lastRunUnique: data.last_run_unique,
    dedupRate: data.dedup_rate,
    refreshIntervalMinutes: data.refresh_interval_minutes,
    isRunning: data.is_running,
  };
}
