"use client";

import { Layers } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

import { EmptyState } from "@/components/ui/empty-state";
import { Pagination } from "@/components/ui/pagination";
import { Skeleton } from "@/components/ui/skeleton";
import { EventClusterCard } from "@/components/events/EventClusterCard";
import { useEvents } from "@/hooks/useEvents";
import { ROUTES } from "@/lib/constants";

const PAGE_SIZE = 12;

export default function EventsPage() {
  const [offset, setOffset] = useState(0);
  const { data, isLoading, isError } = useEvents({
    limit: PAGE_SIZE,
    offset,
  });

  return (
    <div className="mx-auto flex max-w-[1800px] flex-col gap-4 px-4 py-6 lg:px-8 lg:py-8">
      <div>
        <h1 className="text-lg font-medium text-text-primary">Events</h1>
        <p className="text-sm text-text-secondary">
          Every story cluster the pipeline has assembled from the current
          document set.
        </p>
      </div>

      {isLoading && (
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {Array.from({ length: 9 }).map((_, i) => (
            <Skeleton key={i} className="h-36 rounded-(--radius-lg)" />
          ))}
        </div>
      )}

      {isError && (
        <EmptyState
          icon={Layers}
          title="Couldn't load events"
          description="The backend may be unreachable."
        />
      )}

      {data && data.items.length === 0 && (
        <EmptyState
          icon={Layers}
          title="No events yet"
          description="Events appear once the first ingestion cycle finishes clustering documents."
        />
      )}

      {data && data.items.length > 0 && (
        <>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
            {data.items.map((event) => (
              <Link key={event.id} href={`${ROUTES.events}/${event.id}`} className="focus-ring rounded-(--radius-lg)">
                <EventClusterCard event={event} />
              </Link>
            ))}
          </div>

          <Pagination
            offset={data.offset}
            limit={data.limit}
            total={data.total}
            onOffsetChange={setOffset}
          />
        </>
      )}
    </div>
  );
}
