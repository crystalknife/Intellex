"use client";

import { useQuery } from "@tanstack/react-query";

import { getPipelineStats } from "@/lib/api";
import { QUERY_KEYS, REFETCH_INTERVALS, STALE_TIMES } from "@/lib/constants";

export function usePipelineStats() {
  return useQuery({
    queryKey: QUERY_KEYS.pipelineStats(),
    queryFn: getPipelineStats,
    staleTime: STALE_TIMES.pipelineStats,
    refetchInterval: REFETCH_INTERVALS.pipelineStats,
  });
}
