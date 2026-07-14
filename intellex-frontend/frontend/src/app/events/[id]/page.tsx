"use client";

import { ArrowLeft, Layers } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { EntityChip } from "@/components/events/EntityChip";
import { DocumentRow } from "@/components/feed/DocumentRow";
import { useEvent } from "@/hooks/useEvent";
import { formatRelativeTime } from "@/lib/utils";

export default function EventDetailPage() {
  const params = useParams<{ id: string }>();
  const { data: event, isLoading, isError } = useEvent(params.id);

  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-6 px-4 py-6 lg:px-8 lg:py-8">
      <Link
        href="/events"
        className="focus-ring inline-flex w-fit items-center gap-1.5 text-sm text-text-secondary transition-colors duration-(--dur-fast) hover:text-text-primary"
      >
        <ArrowLeft size={14} strokeWidth={1.75} />
        Back to events
      </Link>

      {isLoading && (
        <div className="space-y-3">
          <Skeleton className="h-7 w-2/3" />
          <Skeleton className="h-4 w-1/3" />
          <Skeleton className="h-24 w-full rounded-(--radius-lg)" />
        </div>
      )}

      {isError && (
        <EmptyState
          icon={Layers}
          title="Couldn't load this event"
          description="It may have been re-clustered in a later ingestion cycle, or the backend is unreachable."
        />
      )}

      {event && (
        <>
          <div className="space-y-3">
            <h1 className="text-2xl font-medium text-text-primary">
              {event.title}
            </h1>

            <p className="text-sm text-text-muted">
              {event.documentCount} document
              {event.documentCount === 1 ? "" : "s"} {"\u00b7"} updated{" "}
              {formatRelativeTime(event.updatedAt)}
            </p>

            {Object.keys(event.entities).length > 0 && (
              <div className="flex flex-wrap gap-1.5">
                {Object.entries(event.entities).flatMap(([label, values]) =>
                  values
                    .slice(0, 6)
                    .map((value) => (
                      <EntityChip key={`${label}-${value}`} label={label} name={value} />
                    ))
                )}
              </div>
            )}

            {event.keywords.length > 0 && (
              <p className="text-sm text-text-secondary">
                {event.keywords.join(" \u00b7 ")}
              </p>
            )}
          </div>

          <div className="border-t border-border pt-4">
            <h2 className="mb-2 text-xs font-medium tracking-wide text-text-secondary uppercase">
              Related Documents
            </h2>

            <div className="divide-y divide-border">
              {event.documents.map((document) => (
                <DocumentRow key={document.id} document={document} />
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
