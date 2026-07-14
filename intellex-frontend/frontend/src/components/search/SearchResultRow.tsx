import type { LucideIcon } from "lucide-react";

import { cn } from "@/lib/utils";

interface SearchResultRowProps {
  icon: LucideIcon;
  title: string;
  meta?: string;
  active?: boolean;
  onSelect: () => void;
}

export function SearchResultRow({
  icon: Icon,
  title,
  meta,
  active,
  onSelect,
}: SearchResultRowProps) {
  return (
    <button
      onClick={onSelect}
      role="option"
      aria-selected={active}
      className={cn(
        "focus-ring flex w-full items-center gap-2.5 rounded-(--radius-sm) px-2 py-2 text-left text-sm transition-colors duration-(--dur-instant)",
        active ? "bg-accent-dim text-text-accent" : "text-text-primary hover:bg-glass-2"
      )}
    >
      <Icon size={14} strokeWidth={1.75} className="shrink-0 text-text-muted" />
      <span className="min-w-0 flex-1 truncate">{title}</span>
      {meta && <span className="shrink-0 text-xs text-text-muted">{meta}</span>}
    </button>
  );
}
