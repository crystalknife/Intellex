"use client";

import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";

import { searchDocuments, searchEvents } from "@/lib/api";
import { QUERY_KEYS, STALE_TIMES } from "@/lib/constants";

export function useDebouncedValue<T>(value: T, delayMs = 300): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timeout = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(timeout);
  }, [value, delayMs]);

  return debounced;
}

export function useSearch(query: string) {
  const debounced = useDebouncedValue(query, 300);

  return useQuery({
    queryKey: QUERY_KEYS.search(debounced),
    queryFn: () => searchDocuments(debounced),
    enabled: debounced.trim().length > 0,
    staleTime: STALE_TIMES.search,
  });
}

export function useEventSearch(query: string) {
  const debounced = useDebouncedValue(query, 300);

  return useQuery({
    queryKey: QUERY_KEYS.searchEvents(debounced),
    queryFn: () => searchEvents(debounced),
    enabled: debounced.trim().length > 0,
    staleTime: STALE_TIMES.search,
  });
}
