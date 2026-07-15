import { FileStack } from "lucide-react";
import Link from "next/link";

import { SaveButton } from "@/components/collections/SaveButton";
import { formatRelativeTime, truncate } from "@/lib/utils";
import type { EventCluster } from "@/lib/types";

import { EntityChip } from "./EntityChip";

interface EventClusterCardProps {
  event: EventCluster;
  /** If provided, the card content links here; SaveButton stays a
   * sibling so it's never nested inside the anchor. */
  href?: string;
}

export function EventClusterCard({ event, href }: EventClusterCardProps) {
  const orgs = event.entities.ORG?.slice(0, 2) ?? [];
  const people = event.entities.PERSON?.slice(0, 1) ?? [];

  const body = (
    <>
      <h3 className="pr-7 text-sm leading-snug font-medium text-text-primary">
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
    </>
  );

  return (
    <article className="group relative flex h-full flex-col gap-3 rounded-(--radius-lg) border border-border bg-glass-1 p-4 transition-colors duration-(--dur-fast) hover:border-border-mid">
      <SaveButton
        itemType="event"
        itemId={event.id}
        className="absolute top-3 right-3 opacity-0 transition-opacity duration-(--dur-fast) group-hover:opacity-100 group-focus-within:opacity-100"
      />

      {href ? (
        <Link href={href} className="focus-ring flex h-full flex-col gap-3">
          {body}
        </Link>
      ) : (
        body
      )}
    </article>
  );
}
