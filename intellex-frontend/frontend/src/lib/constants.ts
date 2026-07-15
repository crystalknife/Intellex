export const APP_NAME = "Intellex";

export const APP_DESCRIPTION =
  "AI-powered News Intelligence Platform";

export const SIDEBAR_WIDTH = 240;

export const MAX_CONTENT_WIDTH = 1800;

export const QUERY_KEYS = {
  documents: (params?: object) => ["documents", params ?? {}] as const,
  document: (id: string) => ["documents", id] as const,
  events: (params?: object) => ["events", params ?? {}] as const,
  event: (id: string) => ["events", id] as const,
  search: (query: string) => ["search", query] as const,
  searchEvents: (query: string) => ["search", "events", query] as const,
  pipelineStats: () => ["analytics", "pipeline"] as const,
  currentUser: () => ["auth", "me"] as const,
};

export const STALE_TIMES = {
  documents: 30_000,
  events: 30_000,
  search: 10_000,
  pipelineStats: 15_000,
};

export const REFETCH_INTERVALS = {
  documents: 30_000,
  events: 60_000,
  pipelineStats: 30_000,
};

export const ROUTES = {
  intelligence: "/",
  events: "/events",
  documents: "/documents",
  search: "/search",
  aiWorkspace: "/ai",
  sources: "/sources",
  collections: "/collections",
  timeline: "/timeline",
  settings: "/settings",
  login: "/login",
  signup: "/signup",
};