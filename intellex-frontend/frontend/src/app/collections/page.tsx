"use client";

import { Layers, Plus, Trash2 } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useCollections,
  useCreateCollection,
  useDeleteCollection,
} from "@/hooks/useCollections";
import { formatRelativeTime } from "@/lib/utils";

export default function CollectionsPage() {
  const { data: collections, isLoading, isError } = useCollections();
  const createCollection = useCreateCollection();
  const deleteCollection = useDeleteCollection();

  const [name, setName] = useState("");

  function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) return;

    createCollection.mutate(trimmed, {
      onSuccess: () => setName(""),
    });
  }

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-6 px-4 py-6 lg:px-8 lg:py-8">
      <div>
        <h1 className="text-lg font-medium text-text-primary">Collections</h1>
        <p className="text-sm text-text-secondary">
          Saved documents and events, grouped however you like.
        </p>
      </div>

      <form onSubmit={handleCreate} className="flex gap-2">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="New collection name..."
          className="focus-ring w-full rounded-(--radius-md) border border-border bg-glass-1 px-3 py-2 text-sm text-text-primary placeholder:text-text-muted"
        />
        <button
          type="submit"
          disabled={!name.trim() || createCollection.isPending}
          className="focus-ring inline-flex shrink-0 items-center gap-1.5 rounded-(--radius-md) border border-accent/40 bg-accent-dim px-3 py-2 text-sm font-medium text-text-accent transition-colors duration-(--dur-fast) hover:bg-accent-glow disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Plus size={14} strokeWidth={1.75} />
          Create
        </button>
      </form>

      {isLoading && (
        <div className="space-y-2">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-16 w-full rounded-(--radius-lg)" />
          ))}
        </div>
      )}

      {isError && (
        <EmptyState
          icon={Layers}
          title="Couldn't load collections"
          description="The backend may be unreachable."
        />
      )}

      {collections && collections.length === 0 && (
        <EmptyState
          icon={Layers}
          title="No collections yet"
          description="Create one above, or save a document/event using the bookmark icon anywhere in the app."
        />
      )}

      {collections && collections.length > 0 && (
        <div className="divide-y divide-border rounded-(--radius-lg) border border-border">
          {collections.map((collection) => (
            <div
              key={collection.id}
              className="group flex items-center justify-between gap-4 px-4 py-3"
            >
              <Link
                href={`/collections/${collection.id}`}
                className="focus-ring min-w-0 flex-1"
              >
                <p className="truncate text-sm font-medium text-text-primary">
                  {collection.name}
                </p>
                <p className="text-xs text-text-muted">
                  {collection.itemCount} item
                  {collection.itemCount === 1 ? "" : "s"} {"\u00b7"} updated{" "}
                  {formatRelativeTime(collection.updatedAt)}
                </p>
              </Link>

              <button
                onClick={() => deleteCollection.mutate(collection.id)}
                aria-label={`Delete ${collection.name}`}
                className="focus-ring flex size-7 shrink-0 items-center justify-center rounded-(--radius-sm) text-text-muted opacity-0 transition-colors duration-(--dur-fast) group-hover:opacity-100 hover:bg-glass-2 hover:text-critical"
              >
                <Trash2 size={14} strokeWidth={1.75} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
