import type { LucideIcon } from "lucide-react";

import { cn } from "@/lib/utils";

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center gap-3 rounded-(--radius-lg) border border-border px-6 py-12 text-center",
        className
      )}
    >
      {Icon && (
        <div className="flex size-10 items-center justify-center rounded-full border border-border-mid bg-glass-2 text-text-muted">
          <Icon size={18} strokeWidth={1.75} />
        </div>
      )}

      <div className="space-y-1">
        <p className="text-sm font-medium text-text-primary">{title}</p>
        {description && (
          <p className="max-w-sm text-sm text-text-secondary">
            {description}
          </p>
        )}
      </div>

      {action}
    </div>
  );
}
