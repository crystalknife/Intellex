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

export interface Collection {
  id: string;
  name: string;
  itemCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface CollectionItem {
  id: string;
  type: "document" | "event";
  addedAt: string;
  document: Document | null;
  event: EventCluster | null;
}

export interface CollectionDetail extends Collection {
  items: CollectionItem[];
}

export interface AIStatus {
  configured: boolean;
  model: string;
}

export interface AISource {
  id: string;
  title: string;
  url: string;
  source: string;
}

export interface AIChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: AISource[];
}

export type EntityLabel =
  | "ORG"
  | "PERSON"
  | "GPE"
  | "PRODUCT"
  | "EVENT"
  | string;

export interface User {
  id: string;
  email: string;
  fullName: string;
  createdAt: string;
}

export interface Organization {
  id: string;
  name: string;
  createdAt: string;
}

export type OrganizationRole = "owner" | "admin" | "member";

export interface AuthSession {
  accessToken: string;
  tokenType: string;
  user: User;
  organization: Organization;
  role: OrganizationRole;
}

export interface CurrentUser {
  user: User;
  organization: Organization;
  role: OrganizationRole;
}

export interface OrganizationMember {
  userId: string;
  email: string;
  fullName: string;
  role: OrganizationRole;
  joinedAt: string;
}

export interface OrganizationInvite {
  id: string;
  email: string;
  role: OrganizationRole;
  token: string;
  createdAt: string;
  expiresAt: string;
}
