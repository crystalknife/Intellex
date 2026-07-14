"use client";

import { Wifi } from "lucide-react";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useSources } from "@/hooks/useSources";
import { formatRelativeTime } from "@/lib/utils";

export default function SourcesPage() {
  const { data: sources, isLoading, isError } = useSources();

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-4 px-4 py-6 lg:px-8 lg:py-8">
      <div>
        <h1 className="text-lg font-medium text-text-primary">Sources</h1>
        <p className="text-sm text-text-secondary">
          Every feed currently configured for ingestion, with how much
          each has contributed.
        </p>
      </div>

      {isLoading && (
        <div className="space-y-1.5">
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-12 w-full rounded-(--radius-md)" />
          ))}
        </div>
      )}

      {isError && (
        <EmptyState
          icon={Wifi}
          title="Couldn't load sources"
          description="The backend may be unreachable."
        />
      )}

      {sources && sources.length === 0 && (
        <EmptyState
          icon={Wifi}
          title="No sources yet"
          description="Sources appear once the first ingestion cycle completes."
        />
      )}

      {sources && sources.length > 0 && (
        <div className="divide-y divide-border rounded-(--radius-lg) border border-border">
          {sources.map((source) => (
            <a
              key={source.name}
              href={`/documents?source=${encodeURIComponent(source.name)}`}
              className="focus-ring flex items-center justify-between gap-4 px-4 py-3 text-sm transition-colors duration-(--dur-fast) hover:bg-glass-2"
            >
              <span className="inline-flex items-center gap-2.5 font-medium text-text-primary">
                <span className="size-1.5 rounded-full bg-signal" />
                {source.name}
              </span>

              <span className="flex items-center gap-4 text-xs text-text-muted">
                <span>
                  {source.documentCount} document
                  {source.documentCount === 1 ? "" : "s"}
                </span>
                <span>{formatRelativeTime(source.lastCollectedAt)}</span>
              </span>
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
