import type { LucideIcon } from "lucide-react";

import { cn } from "@/lib/utils";

interface PipelineMetricProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  statusColor?: "positive" | "warning" | "critical" | "neutral";
}

const STATUS_TEXT: Record<string, string> = {
  positive: "text-positive",
  warning: "text-warning",
  critical: "text-critical",
  neutral: "text-neutral",
};

export function PipelineMetric({
  icon: Icon,
  label,
  value,
  statusColor,
}: PipelineMetricProps) {
  return (
    <div className="flex items-center gap-2.5 rounded-(--radius-md) border border-border bg-glass-1 px-3 py-2">
      <Icon
        size={14}
        strokeWidth={1.75}
        className={cn("shrink-0", statusColor ? STATUS_TEXT[statusColor] : "text-text-muted")}
      />
      <div className="flex min-w-0 items-baseline gap-1.5">
        <span className="text-sm font-medium text-text-primary tabular-nums">
          {value}
        </span>
        <span className="truncate text-xs text-text-secondary">{label}</span>
      </div>
    </div>
  );
}
