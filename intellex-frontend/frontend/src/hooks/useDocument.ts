"use client";

import { useQuery } from "@tanstack/react-query";

import { getDocument } from "@/lib/api";
import { QUERY_KEYS, STALE_TIMES } from "@/lib/constants";

export function useDocument(id: string) {
  return useQuery({
    queryKey: QUERY_KEYS.document(id),
    queryFn: () => getDocument(id),
    staleTime: STALE_TIMES.documents,
    enabled: Boolean(id),
  });
}
