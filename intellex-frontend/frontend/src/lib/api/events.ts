import { apiClient } from "@/lib/api/client";
import type { EventCluster, EventDetail, PaginatedResponse } from "@/lib/types";

interface RawEvent {
  id: string;
  title: string;
  summary: string;
  keywords: string[];
  entities: Record<string, string[]>;
  document_count: number;
  created_at: string;
  updated_at: string;
}

interface RawEventDetail extends RawEvent {
  documents: Array<{
    id: string;
    title: string;
    summary: string;
    url: string;
    source: string;
    author: string | null;
    language: string;
    category: string;
    entities: Record<string, string[]>;
    keywords: string[];
    published_at: string | null;
    collected_at: string;
    event_id: string | null;
  }>;
}

interface RawPaginated<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

function toEvent(raw: RawEvent): EventCluster {
  return {
    id: raw.id,
    title: raw.title,
    summary: raw.summary,
    keywords: raw.keywords,
    entities: raw.entities,
    documentCount: raw.document_count,
    createdAt: raw.created_at,
    updatedAt: raw.updated_at,
  };
}

export interface GetEventsParams {
  limit?: number;
  offset?: number;
}

export async function getEvents(
  params: GetEventsParams = {}
): Promise<PaginatedResponse<EventCluster>> {
  const { data } = await apiClient.get<RawPaginated<RawEvent>>("/events/", {
    params,
  });

  return {
    items: data.items.map(toEvent),
    total: data.total,
    limit: data.limit,
    offset: data.offset,
  };
}

export async function searchEvents(
  query: string,
  limit = 20
): Promise<PaginatedResponse<EventCluster>> {
  if (!query.trim()) {
    return { items: [], total: 0, limit, offset: 0 };
  }

  const { data } = await apiClient.get<RawPaginated<RawEvent>>(
    "/search/events",
    { params: { q: query, limit } }
  );

  return {
    items: data.items.map(toEvent),
    total: data.total,
    limit: data.limit,
    offset: data.offset,
  };
}

export async function getEvent(id: string): Promise<EventDetail> {
  const { data } = await apiClient.get<RawEventDetail>(`/events/${id}`);

  return {
    ...toEvent(data),
    documents: data.documents.map((doc) => ({
      id: doc.id,
      title: doc.title,
      summary: doc.summary,
      url: doc.url,
      source: doc.source,
      author: doc.author,
      language: doc.language,
      category: doc.category,
      entities: doc.entities,
      keywords: doc.keywords,
      publishedAt: doc.published_at,
      collectedAt: doc.collected_at,
      eventId: doc.event_id,
    })),
  };
}
