"use client";

import { FeatureErrorBoundary } from "@/components/error/FeatureErrorBoundary";
import { DocumentFeed } from "@/components/feed/DocumentFeed";
import { EventClusterGrid } from "@/components/events/EventClusterGrid";
import { TrendingEntities } from "@/components/entities/TrendingEntities";
import { Divider } from "@/components/ui/divider";

import { IntelligenceBrief } from "./IntelligenceBrief";
import { PipelineStatus } from "./PipelineStatus";

export function IntelligenceWorkspace() {
  return (
    <div className="mx-auto flex max-w-[1800px] flex-col gap-8 px-4 py-6 lg:px-8 lg:py-8">
      <FeatureErrorBoundary name="brief">
        <IntelligenceBrief />
      </FeatureErrorBoundary>

      <FeatureErrorBoundary name="pipeline">
        <section aria-label="Pipeline status">
          <PipelineStatus />
        </section>
      </FeatureErrorBoundary>

      <div className="grid grid-cols-1 gap-8 xl:grid-cols-[1fr_280px]">
        <section aria-labelledby="events-heading" className="min-w-0 space-y-3">
          <h2
            id="events-heading"
            className="text-xs font-medium tracking-wide text-text-secondary uppercase"
          >
            Live Event Clusters
          </h2>

          <FeatureErrorBoundary name="events">
            <EventClusterGrid />
          </FeatureErrorBoundary>
        </section>

        <aside aria-labelledby="entities-heading" className="space-y-3">
          <h2
            id="entities-heading"
            className="text-xs font-medium tracking-wide text-text-secondary uppercase"
          >
            Trending Entities
          </h2>

          <FeatureErrorBoundary name="entities">
            <TrendingEntities />
          </FeatureErrorBoundary>
        </aside>
      </div>

      <Divider />

      <section aria-labelledby="feed-heading" className="space-y-3 pb-8">
        <h2
          id="feed-heading"
          className="text-xs font-medium tracking-wide text-text-secondary uppercase"
        >
          Real-Time Document Feed
        </h2>

        <FeatureErrorBoundary name="feed">
          <DocumentFeed />
        </FeatureErrorBoundary>
      </section>
    </div>
  );
}
