"use client";

import { useQuery } from "@tanstack/react-query";

import { getSources } from "@/lib/api";

export function useSources() {
  return useQuery({
    queryKey: ["sources"] as const,
    queryFn: getSources,
    staleTime: 30_000,
    refetchInterval: 60_000,
  });
}
