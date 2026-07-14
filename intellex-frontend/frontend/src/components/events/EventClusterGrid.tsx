"use client";

import { ArrowRight, Layers } from "lucide-react";
import Link from "next/link";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useEvents } from "@/hooks/useEvents";
import { ROUTES } from "@/lib/constants";
import { sortEventsByRecency } from "@/services/events.service";

import { EventClusterCard } from "./EventClusterCard";

export function EventClusterGrid() {
  const { data, isLoading, isError } = useEvents({ limit: 6 });

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-36 rounded-(--radius-lg)" />
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <EmptyState
        icon={Layers}
        title="Couldn't load event clusters"
        description="The backend may be unreachable. Data will appear once the connection recovers."
      />
    );
  }

  const events = sortEventsByRecency(data?.items ?? []);

  if (events.length === 0) {
    return (
      <EmptyState
        icon={Layers}
        title="No events yet"
        description="Events appear here once the first ingestion cycle finishes clustering documents."
      />
    );
  }

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {events.map((event, index) => (
          <Link
            key={event.id}
            href={`${ROUTES.events}/${event.id}`}
            className="focus-ring enter-animate rounded-(--radius-lg)"
            style={{ animationDelay: `${Math.min(index, 10) * 40}ms` }}
          >
            <EventClusterCard event={event} />
          </Link>
        ))}
      </div>

      {(data?.total ?? 0) > events.length && (
        <Link
          href={ROUTES.events}
          className="focus-ring inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary transition-colors duration-(--dur-fast) hover:text-text-primary"
        >
          View all {data?.total} events
          <ArrowRight size={12} strokeWidth={1.75} />
        </Link>
      )}
    </div>
  );
}
