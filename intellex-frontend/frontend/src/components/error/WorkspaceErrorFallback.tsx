"use client";

import { RefreshCw } from "lucide-react";

export function WorkspaceErrorFallback({
  onRetry,
}: {
  onRetry?: () => void;
}) {
  return (
    <div className="flex h-screen flex-col items-center justify-center gap-4 bg-base px-6 text-center">
      <div className="flex size-12 items-center justify-center rounded-full border border-border-mid bg-glass-2 text-critical">
        <RefreshCw size={20} strokeWidth={1.75} />
      </div>

      <div className="space-y-1">
        <h1 className="text-lg font-medium text-text-primary">
          Intellex hit an unexpected error
        </h1>
        <p className="max-w-sm text-sm text-text-secondary">
          The workspace failed to render. Reloading usually resolves this --
          if it keeps happening, the backend may be unreachable.
        </p>
      </div>

      <button
        onClick={onRetry ?? (() => window.location.reload())}
        className="focus-ring rounded-(--radius-md) border border-border-mid bg-glass-2 px-4 py-2 text-sm font-medium text-text-primary transition-colors duration-(--dur-fast) hover:bg-glass-3"
      >
        Reload workspace
      </button>
    </div>
  );
}
