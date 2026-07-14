"use client";

import { Clock, Copy, Database, Layers, Radio, Wifi } from "lucide-react";

import { Skeleton } from "@/components/ui/skeleton";
import { usePipelineStats } from "@/hooks/usePipelineStats";
import { formatRelativeTime } from "@/lib/utils";

import { PipelineMetric } from "./PipelineMetric";

export function PipelineStatus() {
  const { data: stats, isLoading, isError } = usePipelineStats();

  if (isLoading) {
    return (
      <div className="flex flex-wrap gap-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-9 w-32 rounded-(--radius-md)" />
        ))}
      </div>
    );
  }

  if (isError || !stats) {
    return (
      <p className="text-sm text-text-muted">
        Pipeline status is unavailable right now.
      </p>
    );
  }

  return (
    <div className="enter-animate flex flex-wrap gap-2">
      <PipelineMetric icon={Database} label="Documents" value={stats.totalDocuments} />
      <PipelineMetric icon={Layers} label="Events" value={stats.totalEvents} />
      <PipelineMetric icon={Wifi} label="Sources" value={stats.totalSources} />
      <PipelineMetric icon={Copy} label="Dedup" value={`${stats.dedupRate}%`} />
      <PipelineMetric
        icon={stats.isRunning ? Radio : Clock}
        label={stats.isRunning ? "Ingesting now" : formatRelativeTime(stats.lastRunAt)}
        value={stats.isRunning ? "Live" : "Last run"}
        statusColor={stats.isRunning ? "warning" : "positive"}
      />
    </div>
  );
}
