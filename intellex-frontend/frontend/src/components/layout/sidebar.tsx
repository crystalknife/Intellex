"use client";

import { Hexagon } from "lucide-react";
import Link from "next/link";

import { ROUTES, SIDEBAR_WIDTH } from "@/lib/constants";

import { NavSection } from "./nav-section";
import { navigationSections } from "./navigation";

export function Sidebar() {
  return (
    <aside
      style={{ width: SIDEBAR_WIDTH }}
      className="hidden shrink-0 flex-col border-r border-border bg-surface lg:flex"
    >
      <div className="flex h-14 items-center gap-2 border-b border-border px-4">
        <Link
          href={ROUTES.intelligence}
          className="focus-ring flex items-center gap-2 rounded-(--radius-sm)"
        >
          <Hexagon
            size={18}
            strokeWidth={2}
            className="text-accent"
            fill="var(--color-accent-dim)"
          />
          <span className="text-sm font-semibold tracking-tight text-text-primary">
            Intellex
          </span>
        </Link>
      </div>

      <div className="flex-1 overflow-y-auto py-2">
        {navigationSections.map((section) => (
          <NavSection key={section.label} section={section} />
        ))}
      </div>
    </aside>
  );
}
