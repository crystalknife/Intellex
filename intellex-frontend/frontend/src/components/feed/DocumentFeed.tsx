"use client";

import { ArrowRight, Rss } from "lucide-react";
import Link from "next/link";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useDocuments } from "@/hooks/useDocuments";
import { ROUTES } from "@/lib/constants";

import { DocumentRow } from "./DocumentRow";

export function DocumentFeed() {
  const { data, isLoading, isError } = useDocuments({ limit: 15 });

  if (isLoading) {
    return (
      <div className="space-y-1.5">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} className="h-9 w-full rounded-(--radius-md)" />
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <EmptyState
        icon={Rss}
        title="Couldn't load the document feed"
        description="The backend may be unreachable. Data will appear once the connection recovers."
      />
    );
  }

  const documents = data?.items ?? [];

  if (documents.length === 0) {
    return (
      <EmptyState
        icon={Rss}
        title="No documents yet"
        description="Articles appear here as soon as the first ingestion cycle completes."
      />
    );
  }

  return (
    <div className="space-y-3">
      <div
        className="divide-y divide-border"
        role="feed"
        aria-busy={isLoading}
        aria-label="Real-time document feed"
      >
        {documents.map((document) => (
          <DocumentRow key={document.id} document={document} />
        ))}
      </div>

      {(data?.total ?? 0) > documents.length && (
        <Link
          href={ROUTES.documents}
          className="focus-ring inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary transition-colors duration-(--dur-fast) hover:text-text-primary"
        >
          View all {data?.total} documents
          <ArrowRight size={12} strokeWidth={1.75} />
        </Link>
      )}
    </div>
  );
}
