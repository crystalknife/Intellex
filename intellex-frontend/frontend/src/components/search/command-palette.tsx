"use client";

import { FileText } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { formatRelativeTime } from "@/lib/utils";
import { useSearch } from "@/hooks/useSearch";

import { SearchInput } from "./SearchInput";
import { SearchResultGroup } from "./SearchResultGroup";
import { SearchResultRow } from "./SearchResultRow";

export function CommandPalette({ onClose }: { onClose: () => void }) {
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const { data, isFetching } = useSearch(query);
  const results = data?.items ?? [];

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  function handleQueryChange(value: string) {
    setQuery(value);
    setActiveIndex(0);
  }

  function handleKeyDown(event: React.KeyboardEvent) {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      setActiveIndex((i) => Math.min(i + 1, results.length - 1));
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      setActiveIndex((i) => Math.max(i - 1, 0));
    } else if (event.key === "Enter" && results[activeIndex]) {
      window.open(results[activeIndex].url, "_blank", "noopener,noreferrer");
      onClose();
    } else if (event.key === "Escape") {
      onClose();
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center bg-black/72 pt-[15vh] backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        role="combobox"
        aria-expanded="true"
        className="glass-3 enter-animate w-full max-w-2xl overflow-hidden rounded-(--radius-lg) border border-border-mid"
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
      >
        <SearchInput
          ref={inputRef}
          value={query}
          onChange={(e) => handleQueryChange(e.target.value)}
          placeholder="Search intelligence..."
        />

        <div className="max-h-96 overflow-y-auto py-1">
          {query.trim().length === 0 && (
            <p className="px-4 py-8 text-center text-sm text-text-muted">
              Start typing to search documents
            </p>
          )}

          {query.trim().length > 0 && !isFetching && results.length === 0 && (
            <p className="px-4 py-8 text-center text-sm text-text-muted">
              No results for &ldquo;{query}&rdquo;
            </p>
          )}

          {results.length > 0 && (
            <SearchResultGroup label="Documents">
              {results.map((doc, index) => (
                <SearchResultRow
                  key={doc.id}
                  icon={FileText}
                  title={doc.title}
                  meta={`${doc.source} \u00b7 ${formatRelativeTime(doc.publishedAt)}`}
                  active={index === activeIndex}
                  onSelect={() => {
                    window.open(doc.url, "_blank", "noopener,noreferrer");
                    onClose();
                  }}
                />
              ))}
            </SearchResultGroup>
          )}
        </div>
      </div>
    </div>
  );
}
