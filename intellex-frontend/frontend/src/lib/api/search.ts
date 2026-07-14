import { apiClient } from "@/lib/api/client";
import type { Document, PaginatedResponse } from "@/lib/types";

interface RawDocument {
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
}

interface RawPaginated<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export async function searchDocuments(
  query: string,
  limit = 20
): Promise<PaginatedResponse<Document>> {
  if (!query.trim()) {
    return { items: [], total: 0, limit, offset: 0 };
  }

  const { data } = await apiClient.get<RawPaginated<RawDocument>>(
    "/search/",
    { params: { q: query, limit } }
  );

  return {
    items: data.items.map((raw) => ({
      id: raw.id,
      title: raw.title,
      summary: raw.summary,
      url: raw.url,
      source: raw.source,
      author: raw.author,
      language: raw.language,
      category: raw.category,
      entities: raw.entities,
      keywords: raw.keywords,
      publishedAt: raw.published_at,
      collectedAt: raw.collected_at,
      eventId: raw.event_id,
    })),
    total: data.total,
    limit: data.limit,
    offset: data.offset,
  };
}
