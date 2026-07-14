import type { EventCluster } from "@/lib/types";

export function sortEventsByRecency(events: EventCluster[]): EventCluster[] {
  return [...events].sort(
    (a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
  );
}

/**
 * Flattens entities of a given label (e.g. "ORG") across every event,
 * ranked by how many distinct events mention them -- a rough proxy for
 * "what's trending right now" until a real frequency count is tracked
 * per-document.
 */
export function getTopEntities(
  events: EventCluster[],
  label: string,
  limit = 8
): Array<{ name: string; eventCount: number }> {
  const counts = new Map<string, number>();

  for (const event of events) {
    const values = event.entities[label] ?? [];

    for (const value of new Set(values)) {
      counts.set(value, (counts.get(value) ?? 0) + 1);
    }
  }

  return Array.from(counts.entries())
    .map(([name, eventCount]) => ({ name, eventCount }))
    .sort((a, b) => b.eventCount - a.eventCount)
    .slice(0, limit);
}

export function availableEntityLabels(events: EventCluster[]): string[] {
  const labels = new Set<string>();

  for (const event of events) {
    for (const label of Object.keys(event.entities)) {
      if (event.entities[label]?.length) {
        labels.add(label);
      }
    }
  }

  return Array.from(labels);
}
