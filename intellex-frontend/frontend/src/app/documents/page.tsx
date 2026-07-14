"use client";

import { Rss } from "lucide-react";
import { useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";

import { EmptyState } from "@/components/ui/empty-state";
import { Pagination } from "@/components/ui/pagination";
import { Skeleton } from "@/components/ui/skeleton";
import { DocumentRow } from "@/components/feed/DocumentRow";
import { useDocuments } from "@/hooks/useDocuments";
import { useSources } from "@/hooks/useSources";
import { cn } from "@/lib/utils";

const PAGE_SIZE = 25;

export default function DocumentsPage() {
  return (
    <Suspense fallback={<DocumentsPageSkeleton />}>
      <DocumentsPageContent />
    </Suspense>
  );
}

function DocumentsPageSkeleton() {
  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-4 px-4 py-6 lg:px-8 lg:py-8">
      <div className="space-y-1.5">
        {Array.from({ length: 10 }).map((_, i) => (
          <Skeleton key={i} className="h-9 w-full rounded-(--radius-md)" />
        ))}
      </div>
    </div>
  );
}

function DocumentsPageContent() {
  const searchParams = useSearchParams();
  const [offset, setOffset] = useState(0);
  const [source, setSource] = useState<string | undefined>(
    searchParams.get("source") ?? undefined
  );

  const { data: sources } = useSources();
  const { data, isLoading, isError } = useDocuments({
    limit: PAGE_SIZE,
    offset,
    source,
  });

  function handleSourceChange(next: string | undefined) {
    setSource(next);
    setOffset(0);
  }

  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-4 px-4 py-6 lg:px-8 lg:py-8">
      <div>
        <h1 className="text-lg font-medium text-text-primary">Documents</h1>
        <p className="text-sm text-text-secondary">
          Every article the pipeline has collected and processed.
        </p>
      </div>

      {sources && sources.length > 0 && (
        <div className="flex flex-wrap gap-1.5" role="group" aria-label="Filter by source">
          <button
            onClick={() => handleSourceChange(undefined)}
            className={cn(
              "focus-ring rounded-(--radius-full) border px-2.5 py-1 text-xs font-medium transition-colors duration-(--dur-fast)",
              !source
                ? "border-accent/40 bg-accent-dim text-text-accent"
                : "border-border-mid text-text-secondary hover:text-text-primary"
            )}
          >
            All sources
          </button>

          {sources.map((s) => (
            <button
              key={s.name}
              onClick={() => handleSourceChange(s.name)}
              className={cn(
                "focus-ring rounded-(--radius-full) border px-2.5 py-1 text-xs font-medium transition-colors duration-(--dur-fast)",
                source === s.name
                  ? "border-accent/40 bg-accent-dim text-text-accent"
                  : "border-border-mid text-text-secondary hover:text-text-primary"
              )}
            >
              {s.name} ({s.documentCount})
            </button>
          ))}
        </div>
      )}

      {isLoading && (
        <div className="space-y-1.5">
          {Array.from({ length: 10 }).map((_, i) => (
            <Skeleton key={i} className="h-9 w-full rounded-(--radius-md)" />
          ))}
        </div>
      )}

      {isError && (
        <EmptyState
          icon={Rss}
          title="Couldn't load documents"
          description="The backend may be unreachable."
        />
      )}

      {data && data.items.length === 0 && (
        <EmptyState
          icon={Rss}
          title="No documents found"
          description={source ? `No documents from ${source} yet.` : "Documents appear as soon as the first ingestion cycle completes."}
        />
      )}

      {data && data.items.length > 0 && (
        <>
          <div className="divide-y divide-border">
            {data.items.map((document) => (
              <DocumentRow key={document.id} document={document} />
            ))}
          </div>

          <Pagination
            offset={data.offset}
            limit={data.limit}
            total={data.total}
            onOffsetChange={setOffset}
          />
        </>
      )}
    </div>
  );
}
