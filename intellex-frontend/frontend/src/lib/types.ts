/**
 * Core domain types shared across the app. These mirror the FastAPI
 * response schemas in backend/app/api/schemas/*.py -- keep in sync.
 */

export interface Document {
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
  publishedAt: string | null;
  collectedAt: string;
  eventId: string | null;
}

export interface EventCluster {
  id: string;
  title: string;
  summary: string;
  keywords: string[];
  entities: Record<string, string[]>;
  documentCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface EventDetail extends EventCluster {
  documents: Document[];
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface PipelineStats {
  totalDocuments: number;
  totalEvents: number;
  totalSources: number;
  sources: string[];
  lastRunAt: string | null;
  lastRunFetched: number;
  lastRunUnique: number;
  dedupRate: number;
  refreshIntervalMinutes: number;
  isRunning: boolean;
}

export interface IntelligenceBrief {
  text: string;
  generatedAt: string;
  source: "derived" | "llm";
}

export interface SourceStats {
  name: string;
  documentCount: number;
  lastCollectedAt: string | null;
}

export interface FeedSource {
  id: string;
  url: string;
  label: string;
  enabled: boolean;
  createdAt: string;
}

export type EntityLabel =
  | "ORG"
  | "PERSON"
  | "GPE"
  | "PRODUCT"
  | "EVENT"
  | string;
