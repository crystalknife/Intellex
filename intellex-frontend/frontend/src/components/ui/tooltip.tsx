"use client";

import { useId, useState, type ReactNode } from "react";

import { cn } from "@/lib/utils";

interface TooltipProps {
  content: string;
  children: ReactNode;
  side?: "top" | "right" | "bottom" | "left";
  className?: string;
}

/**
 * Minimal, dependency-free tooltip. Used primarily for "coming soon"
 * hints on disabled nav items -- doesn't need Radix/Base UI's full
 * positioning engine for a single fixed placement.
 */
export function Tooltip({
  content,
  children,
  side = "right",
  className,
}: TooltipProps) {
  const [visible, setVisible] = useState(false);
  const id = useId();

  const sideClasses: Record<string, string> = {
    top: "bottom-full left-1/2 mb-2 -translate-x-1/2",
    bottom: "top-full left-1/2 mt-2 -translate-x-1/2",
    left: "right-full top-1/2 mr-2 -translate-y-1/2",
    right: "left-full top-1/2 ml-2 -translate-y-1/2",
  };

  return (
    <span
      className="relative inline-flex"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
      onFocus={() => setVisible(true)}
      onBlur={() => setVisible(false)}
    >
      {children}
      <span
        id={id}
        role="tooltip"
        className={cn(
          "pointer-events-none absolute z-50 whitespace-nowrap rounded-(--radius-sm) border border-border-mid bg-overlay px-2 py-1 text-xs text-text-secondary shadow-none transition-opacity duration-150",
          sideClasses[side],
          visible ? "opacity-100" : "opacity-0",
          className
        )}
      >
        {content}
      </span>
    </span>
  );
}
