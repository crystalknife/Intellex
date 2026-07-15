"use client";

import { Search, User } from "lucide-react";
import dynamic from "next/dynamic";

import { KeyboardHint } from "@/components/ui/keyboard-hint";
import { LiveDot } from "@/components/ui/live-dot";
import { useCommandPalette } from "@/hooks/useCommandPalette";
import { useLiveIngestion } from "@/hooks/useLiveIngestion";
import { usePipelineStats } from "@/hooks/usePipelineStats";

const CommandPalette = dynamic(
  () =>
    import("@/components/search/command-palette").then(
      (mod) => mod.CommandPalette
    ),
  { ssr: false }
);

export function Topbar() {
  const { open, setOpen } = useCommandPalette();
  const { data: stats } = usePipelineStats();
  const { connectionStatus, isSyncing } = useLiveIngestion();

  const ingesting = isSyncing || stats?.isRunning;

  const dotStatus =
    connectionStatus === "closed"
      ? "critical"
      : ingesting
        ? "warning"
        : "positive";

  const dotLabel =
    connectionStatus === "closed"
      ? "Reconnecting"
      : connectionStatus === "connecting"
        ? "Connecting"
        : ingesting
          ? "Ingesting"
          : "Live";

  return (
    <>
      <header className="flex h-14 shrink-0 items-center justify-between gap-4 border-b border-border bg-base px-4 lg:px-6">
        <button
          onClick={() => setOpen(true)}
          className="focus-ring flex w-full max-w-sm items-center gap-2 rounded-(--radius-md) border border-border bg-glass-1 px-3 py-1.5 text-left text-sm text-text-muted transition-colors duration-(--dur-fast) hover:border-border-mid hover:text-text-secondary"
        >
          <Search size={14} strokeWidth={1.75} />
          <span className="flex-1">Search intelligence...</span>
          <KeyboardHint>⌘K</KeyboardHint>
        </button>

        <div className="flex items-center gap-4">
          <LiveDot status={dotStatus} label={dotLabel} />

          <div className="flex size-7 items-center justify-center rounded-full border border-border-mid bg-glass-2 text-text-secondary">
            <User size={14} strokeWidth={1.75} />
          </div>
        </div>
      </header>

      {open && <CommandPalette onClose={() => setOpen(false)} />}
    </>
  );
}
