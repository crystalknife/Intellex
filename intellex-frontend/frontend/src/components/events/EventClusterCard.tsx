import { FileStack } from "lucide-react";

import { formatRelativeTime, truncate } from "@/lib/utils";
import type { EventCluster } from "@/lib/types";

import { EntityChip } from "./EntityChip";

export function EventClusterCard({ event }: { event: EventCluster }) {
  const orgs = event.entities.ORG?.slice(0, 2) ?? [];
  const people = event.entities.PERSON?.slice(0, 1) ?? [];

  return (
    <article className="group flex h-full flex-col gap-3 rounded-(--radius-lg) border border-border bg-glass-1 p-4 transition-colors duration-(--dur-fast) hover:border-border-mid">
      <h3 className="text-sm leading-snug font-medium text-text-primary">
        {truncate(event.title, 88)}
      </h3>

      {(orgs.length > 0 || people.length > 0) && (
        <div className="flex flex-wrap gap-1.5">
          {orgs.map((org) => (
            <EntityChip key={org} label="ORG" name={org} />
          ))}
          {people.map((person) => (
            <EntityChip key={person} label="PERSON" name={person} />
          ))}
        </div>
      )}

      {event.keywords.length > 0 && (
        <p className="line-clamp-2 text-xs text-text-secondary">
          {event.keywords.slice(0, 6).join(" \u00b7 ")}
        </p>
      )}

      <div className="mt-auto flex items-center justify-between border-t border-border pt-3 text-xs text-text-muted">
        <span className="inline-flex items-center gap-1.5">
          <FileStack size={12} strokeWidth={1.75} />
          {event.documentCount} document{event.documentCount === 1 ? "" : "s"}
        </span>
        <span>{formatRelativeTime(event.updatedAt)}</span>
      </div>
    </article>
  );
}
