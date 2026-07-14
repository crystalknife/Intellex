import { apiClient } from "@/lib/api/client";
import type { SourceStats } from "@/lib/types";

interface RawSourceStats {
  name: string;
  document_count: number;
  last_collected_at: string | null;
}

interface RawSourceListResponse {
  items: RawSourceStats[];
}

export async function getSources(): Promise<SourceStats[]> {
  const { data } = await apiClient.get<RawSourceListResponse>("/sources/");

  return data.items.map((raw) => ({
    name: raw.name,
    documentCount: raw.document_count,
    lastCollectedAt: raw.last_collected_at,
  }));
}
