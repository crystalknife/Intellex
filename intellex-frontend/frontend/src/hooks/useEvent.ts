"use client";

import { useQuery } from "@tanstack/react-query";

import { getEvent } from "@/lib/api";
import { QUERY_KEYS, STALE_TIMES } from "@/lib/constants";

export function useEvent(id: string) {
  return useQuery({
    queryKey: QUERY_KEYS.event(id),
    queryFn: () => getEvent(id),
    staleTime: STALE_TIMES.events,
    enabled: Boolean(id),
  });
}
