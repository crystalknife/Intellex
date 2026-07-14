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

function toDocument(raw: RawDocument): Document {
  return {
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
  };
}

export interface GetDocumentsParams {
  limit?: number;
  offset?: number;
  source?: string;
  category?: string;
}

export async function getDocuments(
  params: GetDocumentsParams = {}
): Promise<PaginatedResponse<Document>> {
  const { data } = await apiClient.get<RawPaginated<RawDocument>>(
    "/documents/",
    { params }
  );

  return {
    items: data.items.map(toDocument),
    total: data.total,
    limit: data.limit,
    offset: data.offset,
  };
}

export async function getDocument(id: string): Promise<Document> {
  const { data } = await apiClient.get<RawDocument>(`/documents/${id}`);

  return toDocument(data);
}
