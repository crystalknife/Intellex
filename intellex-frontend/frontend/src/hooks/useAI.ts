"use client";

import { useMutation, useQuery } from "@tanstack/react-query";

import { askAI, getAIStatus } from "@/lib/api";

export function useAIStatus() {
  return useQuery({
    queryKey: ["ai", "status"],
    queryFn: getAIStatus,
    staleTime: 60_000,
  });
}

export function useAskAI() {
  return useMutation({
    mutationFn: askAI,
  });
}
