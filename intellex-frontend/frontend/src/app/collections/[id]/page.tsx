"use client";

import { ArrowLeft, Layers, X } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { EventClusterCard } from "@/components/events/EventClusterCard";
import { DocumentRow } from "@/components/feed/DocumentRow";
import {
  useCollection,
  useRemoveFromCollection,
  useRenameCollection,
} from "@/hooks/useCollections";
import { ROUTES } from "@/lib/constants";

export default function CollectionDetailPage() {
  const params = useParams<{ id: string }>();
  const { data: collection, isLoading, isError } = useCollection(params.id);
  const renameCollection = useRenameCollection();
  const removeItem = useRemoveFromCollection();

  function handleRename(rawValue: string) {
    const trimmed = rawValue.trim();
    if (!collection || !trimmed || trimmed === collection.name) return;

    renameCollection.mutate({ id: collection.id, name: trimmed });
  }

  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-6 px-4 py-6 lg:px-8 lg:py-8">
      <Link
        href={ROUTES.collections}
        className="focus-ring inline-flex w-fit items-center gap-1.5 text-sm text-text-secondary transition-colors duration-(--dur-fast) hover:text-text-primary"
      >
        <ArrowLeft size={14} strokeWidth={1.75} />
        Back to collections
      </Link>

      {isLoading && (
        <div className="space-y-3">
          <Skeleton className="h-7 w-1/3" />
          <Skeleton className="h-24 w-full rounded-(--radius-lg)" />
        </div>
      )}

      {isError && (
        <EmptyState
          icon={Layers}
          title="Couldn't load this collection"
          description="It may have been deleted, or the backend is unreachable."
        />
      )}

      {collection && (
        <>
          <input
            key={collection.id}
            defaultValue={collection.name}
            onBlur={(e) => handleRename(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") e.currentTarget.blur();
            }}
            className="focus-ring w-full max-w-md rounded-(--radius-md) bg-transparent text-2xl font-medium text-text-primary"
          />

          <p className="-mt-4 text-sm text-text-muted">
            {collection.itemCount} item{collection.itemCount === 1 ? "" : "s"}
          </p>

          {collection.items.length === 0 ? (
            <EmptyState
              icon={Layers}
              title="Nothing saved here yet"
              description="Use the bookmark icon on any document or event to add it to this collection."
            />
          ) : (
            <div className="space-y-3">
              {collection.items.map((item) =>
                item.type === "document" && item.document ? (
                  <div key={item.id} className="flex items-center gap-1">
                    <div className="min-w-0 flex-1">
                      <DocumentRow document={item.document} />
                    </div>
                    <button
                      onClick={() =>
                        removeItem.mutate({
                          collectionId: collection.id,
                          itemId: item.id,
                        })
                      }
                      aria-label="Remove from collection"
                      className="focus-ring flex size-7 shrink-0 items-center justify-center rounded-(--radius-sm) text-text-muted transition-colors duration-(--dur-fast) hover:bg-glass-2 hover:text-critical"
                    >
                      <X size={14} strokeWidth={1.75} />
                    </button>
                  </div>
                ) : item.type === "event" && item.event ? (
                  <div key={item.id} className="relative">
                    <EventClusterCard
                      event={item.event}
                      href={`${ROUTES.events}/${item.event.id}`}
                    />
                    <button
                      onClick={() =>
                        removeItem.mutate({
                          collectionId: collection.id,
                          itemId: item.id,
                        })
                      }
                      aria-label="Remove from collection"
                      className="focus-ring absolute top-3 right-12 flex size-7 items-center justify-center rounded-(--radius-sm) text-text-muted transition-colors duration-(--dur-fast) hover:bg-glass-2 hover:text-critical"
                    >
                      <X size={14} strokeWidth={1.75} />
                    </button>
                  </div>
                ) : null
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}
