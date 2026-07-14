"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createFeed,
  deleteFeed,
  getFeeds,
  setFeedEnabled,
  triggerIngestion,
} from "@/lib/api";

const FEEDS_KEY = ["feeds"] as const;

export function useFeeds() {
  return useQuery({
    queryKey: FEEDS_KEY,
    queryFn: getFeeds,
    staleTime: 30_000,
  });
}

export function useAddFeed() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ url, label }: { url: string; label?: string }) =>
      createFeed(url, label),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: FEEDS_KEY });
    },
  });
}

export function useDeleteFeed() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => deleteFeed(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: FEEDS_KEY });
    },
  });
}

export function useToggleFeed() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, enabled }: { id: string; enabled: boolean }) =>
      setFeedEnabled(id, enabled),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: FEEDS_KEY });
    },
  });
}

export function useTriggerIngestion() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: triggerIngestion,
    onSuccess: () => {
      // The pipeline status strip / brief should reflect "running" soon
      // after this fires -- nudge it to refetch rather than waiting for
      // its own interval.
      queryClient.invalidateQueries({ queryKey: ["analytics", "pipeline"] });
    },
  });
}
