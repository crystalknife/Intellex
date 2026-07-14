"use client";

import { Plus, RefreshCw, Rss, Trash2 } from "lucide-react";
import { useState } from "react";

import { EmptyState } from "@/components/ui/empty-state";
import { LiveDot } from "@/components/ui/live-dot";
import { Skeleton } from "@/components/ui/skeleton";
import {
  useAddFeed,
  useDeleteFeed,
  useFeeds,
  useToggleFeed,
  useTriggerIngestion,
} from "@/hooks/useFeeds";
import { usePipelineStats } from "@/hooks/usePipelineStats";
import { ApiError } from "@/lib/api";
import { cn, formatRelativeTime } from "@/lib/utils";

export default function SettingsPage() {
  const { data: feeds, isLoading, isError } = useFeeds();
  const { data: stats } = usePipelineStats();

  const addFeed = useAddFeed();
  const deleteFeed = useDeleteFeed();
  const toggleFeed = useToggleFeed();
  const trigger = useTriggerIngestion();

  const [url, setUrl] = useState("");
  const [formError, setFormError] = useState<string | null>(null);

  function handleAddFeed(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);

    const trimmed = url.trim();
    if (!trimmed) return;

    addFeed.mutate(
      { url: trimmed },
      {
        onSuccess: () => setUrl(""),
        onError: (error) => {
          setFormError(
            error instanceof ApiError
              ? error.message
              : "Couldn't add that feed."
          );
        },
      }
    );
  }

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-8 px-4 py-6 lg:px-8 lg:py-8">
      <div>
        <h1 className="text-lg font-medium text-text-primary">Settings</h1>
        <p className="text-sm text-text-secondary">
          Configure what Intellex ingests and check on pipeline health.
        </p>
      </div>

      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-medium tracking-wide text-text-secondary uppercase">
            Pipeline
          </h2>

          <button
            onClick={() => trigger.mutate()}
            disabled={trigger.isPending || stats?.isRunning}
            className="focus-ring inline-flex items-center gap-1.5 rounded-(--radius-md) border border-border-mid bg-glass-2 px-3 py-1.5 text-xs font-medium text-text-primary transition-colors duration-(--dur-fast) hover:bg-glass-3 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <RefreshCw
              size={12}
              strokeWidth={1.75}
              className={cn(
                (trigger.isPending || stats?.isRunning) && "animate-spin"
              )}
            />
            {stats?.isRunning ? "Ingesting..." : "Run ingestion now"}
          </button>
        </div>

        {stats && (
          <div className="flex flex-wrap items-center gap-x-6 gap-y-2 rounded-(--radius-lg) border border-border bg-glass-1 px-4 py-3 text-sm">
            <span className="flex items-center gap-2 text-text-secondary">
              <LiveDot status={stats.isRunning ? "warning" : "positive"} />
              {stats.isRunning ? "Running now" : "Idle"}
            </span>
            <span className="text-text-secondary">
              Last run:{" "}
              <span className="text-text-primary">
                {formatRelativeTime(stats.lastRunAt)}
              </span>
            </span>
            <span className="text-text-secondary">
              Refreshes every{" "}
              <span className="text-text-primary">
                {stats.refreshIntervalMinutes}m
              </span>
            </span>
          </div>
        )}

        {trigger.isSuccess && trigger.data.status === "already_running" && (
          <p className="text-xs text-text-muted">
            An ingestion cycle was already in progress.
          </p>
        )}
      </section>

      <section className="space-y-3">
        <h2 className="text-xs font-medium tracking-wide text-text-secondary uppercase">
          Feed Sources
        </h2>

        <form onSubmit={handleAddFeed} className="flex flex-col gap-2">
          <div className="flex gap-2">
            <input
              type="text"
              value={url}
              onChange={(e) => {
                setUrl(e.target.value);
                setFormError(null);
              }}
              placeholder="https://example.com/feed.xml"
              className="focus-ring w-full rounded-(--radius-md) border border-border bg-glass-1 px-3 py-2 text-sm text-text-primary placeholder:text-text-muted"
            />
            <button
              type="submit"
              disabled={addFeed.isPending || !url.trim()}
              className="focus-ring inline-flex shrink-0 items-center gap-1.5 rounded-(--radius-md) border border-accent/40 bg-accent-dim px-3 py-2 text-sm font-medium text-text-accent transition-colors duration-(--dur-fast) hover:bg-accent-glow disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Plus size={14} strokeWidth={1.75} />
              Add
            </button>
          </div>

          {formError && (
            <p className="text-xs text-critical">{formError}</p>
          )}
        </form>

        {isLoading && (
          <div className="space-y-1.5">
            {Array.from({ length: 5 }).map((_, i) => (
              <Skeleton key={i} className="h-11 w-full rounded-(--radius-md)" />
            ))}
          </div>
        )}

        {isError && (
          <EmptyState
            icon={Rss}
            title="Couldn't load feeds"
            description="The backend may be unreachable."
          />
        )}

        {feeds && feeds.length > 0 && (
          <div className="divide-y divide-border rounded-(--radius-lg) border border-border">
            {feeds.map((feed) => (
              <div
                key={feed.id}
                className="flex items-center justify-between gap-4 px-4 py-3"
              >
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm text-text-primary">
                    {feed.label || feed.url}
                  </p>
                  {feed.label && (
                    <p className="truncate text-xs text-text-muted">
                      {feed.url}
                    </p>
                  )}
                </div>

                <div className="flex shrink-0 items-center gap-3">
                  <button
                    onClick={() =>
                      toggleFeed.mutate({
                        id: feed.id,
                        enabled: !feed.enabled,
                      })
                    }
                    className={cn(
                      "focus-ring rounded-(--radius-full) border px-2.5 py-1 text-xs font-medium transition-colors duration-(--dur-fast)",
                      feed.enabled
                        ? "border-positive/30 bg-positive/10 text-positive"
                        : "border-border-mid text-text-muted hover:text-text-secondary"
                    )}
                  >
                    {feed.enabled ? "Enabled" : "Disabled"}
                  </button>

                  <button
                    onClick={() => deleteFeed.mutate(feed.id)}
                    aria-label={`Remove ${feed.label || feed.url}`}
                    className="focus-ring flex size-7 items-center justify-center rounded-(--radius-sm) text-text-muted transition-colors duration-(--dur-fast) hover:bg-glass-2 hover:text-critical"
                  >
                    <Trash2 size={14} strokeWidth={1.75} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        <p className="text-xs text-text-muted">
          Changes here take effect on the next ingestion cycle. Use
          &ldquo;Run ingestion now&rdquo; above to test a new feed
          immediately.
        </p>
      </section>
    </div>
  );
}
