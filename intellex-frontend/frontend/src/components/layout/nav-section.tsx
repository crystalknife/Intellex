"use client";

import { usePathname } from "next/navigation";

import { NavItem } from "./nav-item";
import type { NavigationSection } from "./navigation";

export function NavSection({ section }: { section: NavigationSection }) {
  const pathname = usePathname();

  return (
    <div className="px-3">
      <p className="px-3 pt-4 pb-2 text-[11px] font-medium tracking-wide text-text-muted uppercase">
        {section.label}
      </p>

      <nav className="flex flex-col gap-0.5" aria-label={section.label}>
        {section.items.map((item) => (
          <NavItem
            key={item.name}
            item={item}
            active={pathname === item.href}
          />
        ))}
      </nav>
    </div>
  );
}
