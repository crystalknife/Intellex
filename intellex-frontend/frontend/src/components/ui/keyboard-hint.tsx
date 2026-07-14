import { cn } from "@/lib/utils";

export function KeyboardHint({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <kbd
      className={cn(
        "inline-flex h-5 min-w-5 items-center justify-center rounded-(--radius-xs) border border-border-mid bg-glass-2 px-1.5 font-mono text-[10px] font-medium text-text-secondary",
        className
      )}
    >
      {children}
    </kbd>
  );
}
