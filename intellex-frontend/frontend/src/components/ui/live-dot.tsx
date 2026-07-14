import { cn } from "@/lib/utils";

type LiveDotStatus = "positive" | "warning" | "critical" | "neutral";

const STATUS_COLOR: Record<LiveDotStatus, string> = {
  positive: "bg-positive",
  warning: "bg-warning",
  critical: "bg-critical",
  neutral: "bg-neutral",
};

interface LiveDotProps {
  status?: LiveDotStatus;
  pulse?: boolean;
  className?: string;
  label?: string;
}

export function LiveDot({
  status = "positive",
  pulse = true,
  className,
  label,
}: LiveDotProps) {
  return (
    <span
      className={cn("inline-flex items-center gap-2", className)}
      role={label ? "status" : undefined}
      aria-label={label}
    >
      <span className="relative flex size-2">
        {pulse && (
          <span
            className={cn(
              "absolute inline-flex h-full w-full animate-live-pulse rounded-full opacity-75",
              STATUS_COLOR[status]
            )}
          />
        )}
        <span
          className={cn(
            "relative inline-flex size-2 rounded-full",
            STATUS_COLOR[status]
          )}
        />
      </span>
      {label && <span className="text-xs text-text-secondary">{label}</span>}
    </span>
  );
}
