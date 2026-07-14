import type { ReactNode } from "react";

export function SearchResultGroup({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <div className="px-2 py-2">
      <p className="px-2 pb-1 text-[11px] font-medium tracking-wide text-text-muted uppercase">
        {label}
      </p>
      <div className="flex flex-col gap-0.5">{children}</div>
    </div>
  );
}
