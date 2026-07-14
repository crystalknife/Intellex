export function SourceBadge({ source }: { source: string }) {
  return (
    <span className="inline-flex items-center gap-1.5 text-xs font-medium text-text-secondary">
      <span className="size-1.5 rounded-full bg-signal" />
      {source}
    </span>
  );
}
