"use client";

import { useQuery } from "@tanstack/react-query";

import { getDocuments, type GetDocumentsParams } from "@/lib/api";
import { QUERY_KEYS, REFETCH_INTERVALS, STALE_TIMES } from "@/lib/constants";

export function useDocuments(params: GetDocumentsParams = {}) {
  return useQuery({
    queryKey: QUERY_KEYS.documents(params),
    queryFn: () => getDocuments(params),
    staleTime: STALE_TIMES.documents,
    refetchInterval: REFETCH_INTERVALS.documents,
  });
}
