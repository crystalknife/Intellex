"use client";

import { useState } from "react";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { EntityChip } from "@/components/events/EntityChip";
import { useEvents } from "@/hooks/useEvents";
import { availableEntityLabels, getTopEntities } from "@/services/events.service";
import { Users2 } from "lucide-react";

const LABEL_TITLE: Record<string, string> = {
  ORG: "Organizations",
  PERSON: "People",
  GPE: "Places",
  PRODUCT: "Products",
};

export function TrendingEntities() {
  const { data, isLoading, isError } = useEvents({ limit: 50 });
  const events = data?.items ?? [];
  const labels = availableEntityLabels(events);

  const [activeLabel, setActiveLabel] = useState<string | null>(null);
  const currentLabel = activeLabel && labels.includes(activeLabel)
    ? activeLabel
    : labels[0];

  if (isLoading) {
    return (
      <div className="space-y-2">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-6 w-full rounded-(--radius-sm)" />
        ))}
      </div>
    );
  }

  if (isError || labels.length === 0) {
    return (
      <EmptyState
        icon={Users2}
        title="No entities yet"
        description="Trending entities appear once events have been clustered."
      />
    );
  }

  const entities = getTopEntities(events, currentLabel, 12);

  return (
    <div className="flex flex-col gap-3">
      <div
        className="flex gap-1 border-b border-border pb-2"
        role="tablist"
        aria-label="Entity type"
      >
        {labels.map((label) => (
          <button
            key={label}
            role="tab"
            aria-selected={currentLabel === label}
            onClick={() => setActiveLabel(label)}
            className={`focus-ring rounded-(--radius-sm) px-2.5 py-1 text-xs font-medium transition-colors duration-(--dur-fast) ${
              currentLabel === label
                ? "bg-accent-dim text-text-accent"
                : "text-text-muted hover:text-text-secondary"
            }`}
          >
            {LABEL_TITLE[label] ?? label}
          </button>
        ))}
      </div>

      <div className="flex flex-wrap gap-1.5">
        {entities.map((entity) => (
          <EntityChip key={entity.name} label={currentLabel} name={entity.name} />
        ))}
      </div>
    </div>
  );
}
