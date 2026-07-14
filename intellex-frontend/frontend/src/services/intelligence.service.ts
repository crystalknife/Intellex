import type { Document, EventCluster, IntelligenceBrief } from "@/lib/types";
import { getTopEntities } from "@/services/events.service";

export interface BriefTotals {
  totalDocuments: number;
  totalEvents: number;
  totalSources: number;
}

/**
 * Derives the AI Intelligence Brief from real pipeline data. This has no
 * LLM behind it yet (source: "derived") -- once app/ai/ grows a real
 * provider, swap the implementation of getIntelligenceBrief() in
 * lib/api/ai.ts to call it server-side and this function goes away. The
 * IntelligenceBrief shape and every call site stay identical either way.
 *
 * `documents`/`events` are a recent sample used to derive qualitative
 * highlights (top entities, biggest story); `totals` are the true
 * database-wide counts so the brief's numbers always match the pipeline
 * status strip above it, even when the sample is capped at a page size.
 */
export function deriveIntelligenceBrief(
  documents: Document[],
  events: EventCluster[],
  totals: BriefTotals
): IntelligenceBrief {
  if (totals.totalDocuments === 0) {
    return {
      text: "Waiting on the first ingestion cycle to complete. Intelligence will populate here as soon as documents are collected.",
      generatedAt: new Date().toISOString(),
      source: "derived",
    };
  }

  const topOrgs = getTopEntities(events, "ORG", 3);
  const topPeople = getTopEntities(events, "PERSON", 2);

  const segments: string[] = [];

  segments.push(
    `Tracking ${totals.totalDocuments} document${totals.totalDocuments === 1 ? "" : "s"} across ${totals.totalSources} source${totals.totalSources === 1 ? "" : "s"}, clustered into ${totals.totalEvents} event${totals.totalEvents === 1 ? "" : "s"}.`
  );

  if (topOrgs.length > 0) {
    segments.push(
      `${topOrgs.map((o) => o.name).join(", ")} ${topOrgs.length === 1 ? "leads" : "lead"} organization coverage this cycle.`
    );
  }

  if (topPeople.length > 0) {
    segments.push(
      `Most-mentioned: ${topPeople.map((p) => p.name).join(", ")}.`
    );
  }

  const largestEvent = [...events].sort(
    (a, b) => b.documentCount - a.documentCount
  )[0];

  if (largestEvent && largestEvent.documentCount > 1) {
    segments.push(
      `"${largestEvent.title}" is the most-covered story right now, with ${largestEvent.documentCount} related articles.`
    );
  }

  return {
    text: segments.join(" "),
    generatedAt: new Date().toISOString(),
    source: "derived",
  };
}
