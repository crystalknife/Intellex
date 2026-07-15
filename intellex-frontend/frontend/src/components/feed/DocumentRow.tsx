import { ArrowUpRight } from "lucide-react";

import { SaveButton } from "@/components/collections/SaveButton";
import { formatRelativeTime, truncate } from "@/lib/utils";
import type { Document } from "@/lib/types";

import { SourceBadge } from "./SourceBadge";

export function DocumentRow({ document }: { document: Document }) {
  return (
    <div className="group flex items-center gap-1 rounded-(--radius-md) px-1 transition-colors duration-(--dur-fast) hover:bg-glass-2">
      <a
        href={document.url}
        target="_blank"
        rel="noopener noreferrer"
        className="focus-ring flex min-w-0 flex-1 items-center gap-3 rounded-(--radius-md) px-2 py-2 text-sm"
      >
        <div className="w-28 shrink-0">
          <SourceBadge source={document.source} />
        </div>

        <span className="min-w-0 flex-1 truncate text-text-primary">
          {truncate(document.title, 96)}
        </span>

        {document.category && (
          <span className="hidden shrink-0 text-xs text-text-muted sm:inline">
            {document.category}
          </span>
        )}

        <span className="shrink-0 text-xs text-text-muted tabular-nums">
          {formatRelativeTime(document.publishedAt ?? document.collectedAt)}
        </span>

        <ArrowUpRight
          size={13}
          strokeWidth={1.75}
          className="shrink-0 text-text-disabled opacity-0 transition-opacity duration-(--dur-fast) group-hover:opacity-100"
        />
      </a>

      <SaveButton
        itemType="document"
        itemId={document.id}
        className="shrink-0 opacity-0 transition-opacity duration-(--dur-fast) group-hover:opacity-100 group-focus-within:opacity-100"
      />
    </div>
  );
}
