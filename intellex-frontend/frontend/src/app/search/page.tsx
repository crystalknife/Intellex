"use client";

import { Search as SearchIcon } from "lucide-react";
import { useState } from "react";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { DocumentRow } from "@/components/feed/DocumentRow";
import { useSearch } from "@/hooks/useSearch";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const { data, isFetching } = useSearch(query);

  const trimmed = query.trim();
  const results = data?.items ?? [];

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-4 px-4 py-6 lg:px-8 lg:py-8">
      <div>
        <h1 className="text-lg font-medium text-text-primary">Search</h1>
        <p className="text-sm text-text-secondary">
          Search across every collected document by title, summary, or
          content.
        </p>
      </div>

      <div className="flex items-center gap-2.5 rounded-(--radius-md) border border-border bg-glass-1 px-3 py-2.5">
        <SearchIcon size={15} strokeWidth={1.75} className="shrink-0 text-text-muted" />
        <input
          autoFocus
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search intelligence..."
          className="w-full bg-transparent text-[15px] text-text-primary placeholder:text-text-muted focus:outline-none"
        />
      </div>

      {trimmed.length === 0 && (
        <p className="py-8 text-center text-sm text-text-muted">
          Start typing to search documents
        </p>
      )}

      {trimmed.length > 0 && isFetching && (
        <div className="space-y-1.5">
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-9 w-full rounded-(--radius-md)" />
          ))}
        </div>
      )}

      {trimmed.length > 0 && !isFetching && results.length === 0 && (
        <EmptyState
          icon={SearchIcon}
          title="No results"
          description={`Nothing matched "${trimmed}".`}
        />
      )}

      {results.length > 0 && (
        <div className="divide-y divide-border">
          {results.map((document) => (
            <DocumentRow key={document.id} document={document} />
          ))}
        </div>
      )}
    </div>
  );
}
