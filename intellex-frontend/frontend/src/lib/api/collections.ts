import { apiClient } from "@/lib/api/client";
import type {
  Collection,
  CollectionDetail,
  CollectionItem,
  Document,
  EventCluster,
} from "@/lib/types";

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

interface RawCollection {
  id: string;
  name: string;
  item_count: number;
  created_at: string;
  updated_at: string;
}

interface RawCollectionItem {
  id: string;
  type: "document" | "event";
  added_at: string;
  document: RawDocument | null;
  event: RawEvent | null;
}

interface RawCollectionDetail extends RawCollection {
  items: RawCollectionItem[];
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

function toCollection(raw: RawCollection): Collection {
  return {
    id: raw.id,
    name: raw.name,
    itemCount: raw.item_count,
    createdAt: raw.created_at,
    updatedAt: raw.updated_at,
  };
}

function toCollectionItem(raw: RawCollectionItem): CollectionItem {
  return {
    id: raw.id,
    type: raw.type,
    addedAt: raw.added_at,
    document: raw.document ? toDocument(raw.document) : null,
    event: raw.event ? toEvent(raw.event) : null,
  };
}

export async function getCollections(): Promise<Collection[]> {
  const { data } = await apiClient.get<{ items: RawCollection[] }>(
    "/collections/"
  );

  return data.items.map(toCollection);
}

export async function getCollection(id: string): Promise<CollectionDetail> {
  const { data } = await apiClient.get<RawCollectionDetail>(
    `/collections/${id}`
  );

  return {
    ...toCollection(data),
    items: data.items.map(toCollectionItem),
  };
}

export async function createCollection(name: string): Promise<Collection> {
  const { data } = await apiClient.post<RawCollection>("/collections/", {
    name,
  });

  return toCollection(data);
}

export async function renameCollection(
  id: string,
  name: string
): Promise<Collection> {
  const { data } = await apiClient.patch<RawCollection>(
    `/collections/${id}`,
    { name }
  );

  return toCollection(data);
}

export async function deleteCollection(id: string): Promise<void> {
  await apiClient.delete(`/collections/${id}`);
}

export async function addToCollection(
  collectionId: string,
  type: "document" | "event",
  itemId: string
): Promise<CollectionItem> {
  const { data } = await apiClient.post<RawCollectionItem>(
    `/collections/${collectionId}/items`,
    { type, id: itemId }
  );

  return toCollectionItem(data);
}

export async function removeFromCollection(
  collectionId: string,
  itemId: string
): Promise<void> {
  await apiClient.delete(`/collections/${collectionId}/items/${itemId}`);
}
