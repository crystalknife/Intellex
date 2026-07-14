export function SkipToContent() {
  return (
    <a
      href="#main-content"
      className="focus-ring sr-only rounded-(--radius-md) border border-border-mid bg-overlay px-4 py-2 text-sm font-medium text-text-primary focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[100]"
    >
      Skip to content
    </a>
  );
}
