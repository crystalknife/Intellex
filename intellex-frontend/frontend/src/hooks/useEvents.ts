"use client";

import { useQuery } from "@tanstack/react-query";

import { getEvents, type GetEventsParams } from "@/lib/api";
import { QUERY_KEYS, REFETCH_INTERVALS, STALE_TIMES } from "@/lib/constants";

export function useEvents(params: GetEventsParams = {}) {
  return useQuery({
    queryKey: QUERY_KEYS.events(params),
    queryFn: () => getEvents(params),
    staleTime: STALE_TIMES.events,
    refetchInterval: REFETCH_INTERVALS.events,
  });
}
