import { apiClient } from "@/lib/api/client";
import type { FeedSource } from "@/lib/types";

interface RawFeedSource {
  id: string;
  url: string;
  label: string;
  enabled: boolean;
  created_at: string;
}

function toFeedSource(raw: RawFeedSource): FeedSource {
  return {
    id: raw.id,
    url: raw.url,
    label: raw.label,
    enabled: raw.enabled,
    createdAt: raw.created_at,
  };
}

export async function getFeeds(): Promise<FeedSource[]> {
  const { data } = await apiClient.get<{ items: RawFeedSource[] }>(
    "/feeds/"
  );

  return data.items.map(toFeedSource);
}

export async function createFeed(
  url: string,
  label = ""
): Promise<FeedSource> {
  const { data } = await apiClient.post<RawFeedSource>("/feeds/", {
    url,
    label,
  });

  return toFeedSource(data);
}

export async function deleteFeed(id: string): Promise<void> {
  await apiClient.delete(`/feeds/${id}`);
}

export async function setFeedEnabled(
  id: string,
  enabled: boolean
): Promise<FeedSource> {
  const { data } = await apiClient.patch<RawFeedSource>(`/feeds/${id}`, {
    enabled,
  });

  return toFeedSource(data);
}

export async function triggerIngestion(): Promise<{ status: string }> {
  const { data } = await apiClient.post<{ status: string }>(
    "/ingestion/trigger"
  );

  return data;
}
