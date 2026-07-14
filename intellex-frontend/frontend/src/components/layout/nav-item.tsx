import Link from "next/link";

import { cn } from "@/lib/utils";
import { Tooltip } from "@/components/ui/tooltip";

import type { NavigationItem } from "./navigation";

interface NavItemProps {
  item: NavigationItem;
  active: boolean;
}

export function NavItem({ item, active }: NavItemProps) {
  const Icon = item.icon;

  const content = (
    <span
      className={cn(
        "group flex w-full items-center gap-3 rounded-(--radius-md) px-3 py-2 text-sm transition-colors duration-(--dur-fast)",
        active
          ? "bg-accent-dim text-text-accent"
          : "text-text-secondary hover:bg-glass-2 hover:text-text-primary",
        item.disabled && "cursor-default text-text-disabled hover:bg-transparent hover:text-text-disabled"
      )}
    >
      <Icon size={16} strokeWidth={1.75} />
      <span className="truncate">{item.name}</span>
    </span>
  );

  if (item.disabled) {
    return (
      <Tooltip content="Coming soon" side="right">
        <span aria-disabled="true">{content}</span>
      </Tooltip>
    );
  }

  return (
    <Link href={item.href} aria-current={active ? "page" : undefined}>
      {content}
    </Link>
  );
}
