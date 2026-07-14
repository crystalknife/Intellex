"use client";

import { Sparkles } from "lucide-react";

import { Skeleton } from "@/components/ui/skeleton";
import { useIntelligenceBrief } from "@/hooks/useIntelligenceBrief";

export function IntelligenceBrief() {
  const { data: brief, isLoading, isError } = useIntelligenceBrief();

  return (
    <section
      aria-labelledby="intelligence-brief-heading"
      className="enter-animate rounded-(--radius-lg) border border-border bg-glass-1 p-5"
    >
      <div className="mb-3 flex items-center gap-2">
        <Sparkles size={14} strokeWidth={1.75} className="text-accent" />
        <h2
          id="intelligence-brief-heading"
          className="text-xs font-medium tracking-wide text-text-secondary uppercase"
        >
          Today&apos;s Intelligence
        </h2>
      </div>

      {isLoading && (
        <div className="space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-2/3" />
        </div>
      )}

      {isError && (
        <p className="text-sm text-text-muted">
          Intelligence brief is unavailable right now.
        </p>
      )}

      {brief && (
        <p className="text-[15px] leading-relaxed text-text-primary">
          {brief.text}
        </p>
      )}
    </section>
  );
}
