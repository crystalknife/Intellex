"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";

import { cn } from "@/lib/utils";

interface PaginationProps {
  offset: number;
  limit: number;
  total: number;
  onOffsetChange: (offset: number) => void;
  className?: string;
}

export function Pagination({
  offset,
  limit,
  total,
  onOffsetChange,
  className,
}: PaginationProps) {
  const currentPage = Math.floor(offset / limit) + 1;
  const totalPages = Math.max(1, Math.ceil(total / limit));
  const rangeStart = total === 0 ? 0 : offset + 1;
  const rangeEnd = Math.min(offset + limit, total);

  return (
    <div
      className={cn(
        "flex items-center justify-between border-t border-border pt-4 text-sm",
        className
      )}
    >
      <p className="text-text-secondary">
        {rangeStart}&ndash;{rangeEnd} of {total}
      </p>

      <div className="flex items-center gap-2">
        <button
          onClick={() => onOffsetChange(Math.max(0, offset - limit))}
          disabled={currentPage <= 1}
          className="focus-ring flex size-7 items-center justify-center rounded-(--radius-sm) border border-border-mid text-text-secondary transition-colors duration-(--dur-fast) hover:bg-glass-2 disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:bg-transparent"
          aria-label="Previous page"
        >
          <ChevronLeft size={14} strokeWidth={1.75} />
        </button>

        <span className="min-w-16 text-center text-xs text-text-muted tabular-nums">
          Page {currentPage} of {totalPages}
        </span>

        <button
          onClick={() => onOffsetChange(offset + limit)}
          disabled={currentPage >= totalPages}
          className="focus-ring flex size-7 items-center justify-center rounded-(--radius-sm) border border-border-mid text-text-secondary transition-colors duration-(--dur-fast) hover:bg-glass-2 disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:bg-transparent"
          aria-label="Next page"
        >
          <ChevronRight size={14} strokeWidth={1.75} />
        </button>
      </div>
    </div>
  );
}
