"use client";

import { Bookmark, Check, Plus } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { useAddToCollection, useCollections, useCreateCollection } from "@/hooks/useCollections";
import { ApiError } from "@/lib/api";
import { cn } from "@/lib/utils";

interface SaveButtonProps {
  itemType: "document" | "event";
  itemId: string;
  className?: string;
}

/**
 * Bookmark-style button that opens a small popover for saving a
 * document or event to an existing collection, or creating a new one
 * inline. Used from DocumentRow and EventClusterCard.
 */
export function SaveButton({ itemType, itemId, className }: SaveButtonProps) {
  const [open, setOpen] = useState(false);
  const [newName, setNewName] = useState("");
  const [savedTo, setSavedTo] = useState<Set<string>>(new Set());
  const [duplicateOf, setDuplicateOf] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const { data: collections } = useCollections();
  const addToCollection = useAddToCollection();
  const createCollection = useCreateCollection();

  useEffect(() => {
    if (!open) return;

    function handleClickOutside(event: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  function handleSave(collectionId: string) {
    setDuplicateOf(null);

    addToCollection.mutate(
      { collectionId, type: itemType, itemId },
      {
        onSuccess: () => {
          setSavedTo((prev) => new Set(prev).add(collectionId));
        },
        onError: (error) => {
          if (error instanceof ApiError && error.status === 409) {
            setSavedTo((prev) => new Set(prev).add(collectionId));
            setDuplicateOf(collectionId);
          }
        },
      }
    );
  }

  function handleCreateAndSave(e: React.FormEvent) {
    e.preventDefault();

    const trimmed = newName.trim();
    if (!trimmed) return;

    createCollection.mutate(trimmed, {
      onSuccess: (collection) => {
        setNewName("");
        handleSave(collection.id);
      },
    });
  }

  return (
    <div ref={containerRef} className={cn("relative", className)}>
      <button
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          setOpen((prev) => !prev);
        }}
        aria-label="Save to collection"
        aria-expanded={open}
        className="focus-ring flex size-7 items-center justify-center rounded-(--radius-sm) text-text-muted transition-colors duration-(--dur-fast) hover:bg-glass-2 hover:text-text-primary"
      >
        <Bookmark size={14} strokeWidth={1.75} />
      </button>

      {open && (
        <div
          onClick={(e) => e.stopPropagation()}
          className="glass-3 absolute top-full right-0 z-40 mt-1 w-64 overflow-hidden rounded-(--radius-lg) border border-border-mid"
        >
          <div className="max-h-48 overflow-y-auto p-1">
            {collections && collections.length > 0 ? (
              collections.map((collection) => {
                const saved = savedTo.has(collection.id);

                return (
                  <button
                    key={collection.id}
                    onClick={() => handleSave(collection.id)}
                    disabled={saved}
                    className="focus-ring flex w-full items-center justify-between gap-2 rounded-(--radius-sm) px-2.5 py-2 text-left text-sm text-text-primary transition-colors duration-(--dur-instant) hover:bg-glass-2 disabled:cursor-default"
                  >
                    <span className="min-w-0 flex-1 truncate">
                      {collection.name}
                    </span>
                    {saved ? (
                      <Check size={13} strokeWidth={2} className="shrink-0 text-positive" />
                    ) : (
                      <span className="shrink-0 text-xs text-text-muted">
                        {collection.itemCount}
                      </span>
                    )}
                  </button>
                );
              })
            ) : (
              <p className="px-2.5 py-3 text-xs text-text-muted">
                No collections yet.
              </p>
            )}
          </div>

          {duplicateOf && (
            <p className="border-t border-border px-2.5 py-1.5 text-xs text-text-muted">
              Already saved there
            </p>
          )}

          <form
            onSubmit={handleCreateAndSave}
            className="flex items-center gap-1.5 border-t border-border p-1.5"
          >
            <input
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="New collection..."
              className="focus-ring w-full rounded-(--radius-sm) bg-transparent px-2 py-1.5 text-sm text-text-primary placeholder:text-text-muted"
            />
            <button
              type="submit"
              disabled={!newName.trim() || createCollection.isPending}
              aria-label="Create collection"
              className="focus-ring flex size-7 shrink-0 items-center justify-center rounded-(--radius-sm) text-text-muted transition-colors duration-(--dur-fast) hover:bg-glass-2 hover:text-text-primary disabled:opacity-40"
            >
              <Plus size={14} strokeWidth={1.75} />
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
