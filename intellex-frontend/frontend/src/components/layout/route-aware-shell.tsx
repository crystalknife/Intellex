"use client";

import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

// Routes that render full-bleed, without the sidebar/topbar chrome --
// showing a signed-out person a nav full of workspace links (and a
// "Live" indicator, search bar, etc.) around a login form is wrong.
// This list stays short and explicit rather than trying to be clever
// about "is this an app route" -- Phase B's route protection can lean
// on this same list if it grows.
const CHROMELESS_ROUTES = ["/login", "/signup"];

export function RouteAwareShell({
  shell,
  children,
}: {
  shell: ReactNode;
  children: ReactNode;
}) {
  const pathname = usePathname();
  const isChromeless = CHROMELESS_ROUTES.some((route) =>
    pathname?.startsWith(route)
  );

  return isChromeless ? <>{children}</> : <>{shell}</>;
}
