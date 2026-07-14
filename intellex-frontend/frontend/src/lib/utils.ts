import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * "3m ago", "2h ago", "5d ago" -- falls back to a short absolute date
 * once something is old enough that "ago" stops being useful.
 */
export function formatRelativeTime(iso: string | null | undefined): string {
  if (!iso) return "unknown";

  const date = new Date(iso);
  const diffMs = Date.now() - date.getTime();

  if (Number.isNaN(diffMs)) return "unknown";
  if (diffMs < 0) return "just now";

  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (seconds < 45) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  if (days < 7) return `${days}d ago`;

  return formatAbsoluteTime(iso, { short: true });
}

export function formatAbsoluteTime(
  iso: string | null | undefined,
  options?: { short?: boolean }
): string {
  if (!iso) return "unknown";

  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "unknown";

  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: options?.short ? undefined : "numeric",
    hour: options?.short ? undefined : "numeric",
    minute: options?.short ? undefined : "2-digit",
  }).format(date);
}

const ENTITY_COLOR_VAR: Record<string, string> = {
  ORG: "var(--color-entity-org)",
  PERSON: "var(--color-entity-person)",
  GPE: "var(--color-entity-gpe)",
  LOC: "var(--color-entity-gpe)",
  PRODUCT: "var(--color-entity-product)",
  EVENT: "var(--color-entity-event)",
};

export function getEntityColor(label: string): string {
  return ENTITY_COLOR_VAR[label] ?? "var(--color-entity-other)";
}

export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength - 1).trimEnd()}\u2026`;
}
