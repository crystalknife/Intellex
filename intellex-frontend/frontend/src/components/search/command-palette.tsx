"use client";

import { FileText, Layers, Sparkles } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import { formatRelativeTime } from "@/lib/utils";
import { useEventSearch, useSearch } from "@/hooks/useSearch";

import { SearchInput } from "./SearchInput";
import { SearchResultGroup } from "./SearchResultGroup";
import { SearchResultRow } from "./SearchResultRow";

interface PaletteItem {
  id: string;
  title: string;
  meta?: string;
  onSelect: () => void;
}

export function CommandPalette({ onClose }: { onClose: () => void }) {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const { data: docData, isFetching: docsFetching } = useSearch(query);
  const { data: eventData, isFetching: eventsFetching } = useEventSearch(query);

  const documents = docData?.items ?? [];
  const events = eventData?.items ?? [];
  const isFetching = docsFetching || eventsFetching;
  const trimmedQuery = query.trim();

  const documentItems: PaletteItem[] = documents.map((doc) => ({
    id: doc.id,
    title: doc.title,
    meta: `${doc.source} \u00b7 ${formatRelativeTime(doc.publishedAt)}`,
    onSelect: () => {
      window.open(doc.url, "_blank", "noopener,noreferrer");
      onClose();
    },
  }));

  const eventItems: PaletteItem[] = events.map((event) => ({
    id: event.id,
    title: event.title,
    meta: `${event.documentCount} documents \u00b7 ${formatRelativeTime(event.updatedAt)}`,
    onSelect: () => {
      router.push(`/events/${event.id}`);
      onClose();
    },
  }));

  const actionItems: PaletteItem[] =
    trimmedQuery.length > 0
      ? [
          {
            id: "ask-intellex",
            title: `Ask Intellex about "${trimmedQuery}"`,
            onSelect: () => {
              router.push(`/ai?q=${encodeURIComponent(trimmedQuery)}`);
              onClose();
            },
          },
        ]
      : [];

  const items = [...documentItems, ...eventItems, ...actionItems];
  const hasResults = documentItems.length > 0 || eventItems.length > 0;

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
      setActiveIndex((i) => Math.min(i + 1, items.length - 1));
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      setActiveIndex((i) => Math.max(i - 1, 0));
    } else if (event.key === "Tab") {
      event.preventDefault();
      const boundaries = [
        0,
        documentItems.length,
        documentItems.length + eventItems.length,
      ].filter((b) => b < items.length);
      const next = boundaries.find((b) => b > activeIndex) ?? boundaries[0] ?? 0;
      setActiveIndex(next);
    } else if (event.key === "Enter" && items[activeIndex]) {
      items[activeIndex].onSelect();
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
          {trimmedQuery.length === 0 && (
            <p className="px-4 py-8 text-center text-sm text-text-muted">
              Start typing to search documents, events, and intelligence
            </p>
          )}

          {trimmedQuery.length > 0 && !isFetching && !hasResults && (
            <p className="px-4 py-6 text-center text-sm text-text-muted">
              No documents or events for &ldquo;{trimmedQuery}&rdquo;
            </p>
          )}

          {documentItems.length > 0 && (
            <SearchResultGroup label="Documents">
              {documentItems.map((item, i) => (
                <SearchResultRow
                  key={item.id}
                  icon={FileText}
                  title={item.title}
                  meta={item.meta}
                  active={i === activeIndex}
                  onSelect={item.onSelect}
                />
              ))}
            </SearchResultGroup>
          )}

          {eventItems.length > 0 && (
            <SearchResultGroup label="Events">
              {eventItems.map((item, localIndex) => (
                <SearchResultRow
                  key={item.id}
                  icon={Layers}
                  title={item.title}
                  meta={item.meta}
                  active={documentItems.length + localIndex === activeIndex}
                  onSelect={item.onSelect}
                />
              ))}
            </SearchResultGroup>
          )}

          {actionItems.length > 0 && (
            <SearchResultGroup label="Intelligence">
              {actionItems.map((item, localIndex) => (
                <SearchResultRow
                  key={item.id}
                  icon={Sparkles}
                  title={item.title}
                  active={
                    documentItems.length + eventItems.length + localIndex ===
                    activeIndex
                  }
                  onSelect={item.onSelect}
                />
              ))}
            </SearchResultGroup>
          )}
        </div>
      </div>
    </div>
  );
}
