"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import type { ReactNode } from "react";

import { useCurrentUser } from "@/hooks/useAuth";
import { getStoredToken } from "@/lib/api/auth";
import { ROUTES } from "@/lib/constants";

// Routes that render full-bleed, without the sidebar/topbar chrome, and
// without the auth gate below -- a signed-out person needs to be able
// to reach these.
const CHROMELESS_ROUTES = ["/login", "/signup"];

/**
 * Two jobs: (1) skip the AppShell chrome on auth pages (unchanged from
 * Phase A), and (2) gate every other route behind a valid session,
 * redirecting to /login when there isn't one -- Phase B's routers now
 * require auth, so an ungated frontend would just show a workspace full
 * of 401 errors instead of a login prompt.
 *
 * localStorage is only readable client-side, so `hasToken` starts as
 * `null` and is set in an effect after mount rather than read directly
 * during render -- reading it during render would make the server-
 * rendered HTML and the client's first hydration pass disagree.
 */
export function RouteAwareShell({
  shell,
  children,
}: {
  shell: ReactNode;
  children: ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const isChromeless = CHROMELESS_ROUTES.some((route) =>
    pathname?.startsWith(route)
  );

  const [hasToken, setHasToken] = useState<boolean | null>(null);

  useEffect(() => {
    setHasToken(Boolean(getStoredToken()));
  }, [pathname]);

  const { isLoading, isError } = useCurrentUser();

  useEffect(() => {
    if (isChromeless) return;
    if (hasToken === false) {
      router.replace(ROUTES.login);
    }
  }, [isChromeless, hasToken, router]);

  if (isChromeless) {
    return <>{children}</>;
  }

  if (hasToken === null || hasToken === false) {
    // Either not yet determined (pre-hydration) or a redirect is
    // already in flight -- render nothing rather than flash the app
    // shell for a visitor who isn't signed in.
    return null;
  }

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-base text-sm text-text-muted">
        Loading your workspace...
      </div>
    );
  }

  if (isError) {
    // Token is present but invalid/expired -- the apiClient response
    // interceptor already triggers a hard redirect to /login for this
    // case (see lib/api/client.ts), so there's nothing to do here
    // except avoid rendering the shell in the brief moment before that
    // redirect happens.
    return null;
  }

  return <>{shell}</>;
}
