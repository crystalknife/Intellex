"use client";

import { LogOut, User as UserIcon } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import {
  DropdownMenu,
  DropdownMenuContent,
<<<<<<< HEAD
=======
  DropdownMenuGroup,
>>>>>>> 76704d7 (feat: add AI workspace, authentication, collections, and platform infrastructure)
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useCurrentUser, useLogout } from "@/hooks/useAuth";
import { ROUTES } from "@/lib/constants";

/**
 * Phase A doesn't gate any routes yet, so this renders for both signed-in
 * and signed-out visitors -- a signed-out person sees a plain sign-in
 * link instead of a menu with nothing useful in it.
 */
export function AccountMenu() {
  const { data } = useCurrentUser();
  const logout = useLogout();
  const router = useRouter();

  function handleLogout() {
    logout();
    router.push(ROUTES.login);
  }

  if (!data) {
    return (
      <Link
        href={ROUTES.login}
        aria-label="Sign in"
        className="focus-ring flex size-7 items-center justify-center rounded-full border border-border-mid bg-glass-2 text-text-secondary transition-colors duration-(--dur-fast) hover:text-text-primary"
      >
        <UserIcon size={14} strokeWidth={1.75} />
      </Link>
    );
  }

  const initials = (data.user.fullName.trim() || data.user.email)
    .charAt(0)
    .toUpperCase();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger
        aria-label="Account menu"
        className="focus-ring flex size-7 items-center justify-center rounded-full border border-accent/40 bg-accent-dim text-xs font-medium text-text-accent transition-colors duration-(--dur-fast) hover:bg-accent-glow"
      >
        {initials}
      </DropdownMenuTrigger>

      <DropdownMenuContent
        align="end"
        sideOffset={8}
        className="w-64 rounded-(--radius-lg) border border-border-mid bg-overlay p-1 text-text-primary shadow-lg"
      >
<<<<<<< HEAD
        <DropdownMenuLabel className="px-2 py-1.5 text-text-primary">
          <p className="truncate text-sm font-medium">
            {data.user.fullName || data.user.email}
          </p>
          <p className="truncate text-xs text-text-muted">
            {data.user.email}
          </p>
        </DropdownMenuLabel>
=======
        <DropdownMenuGroup>
          <DropdownMenuLabel className="px-2 py-1.5 text-text-primary">
            <p className="truncate text-sm font-medium">
              {data.user.fullName || data.user.email}
            </p>
            <p className="truncate text-xs text-text-muted">
              {data.user.email}
            </p>
          </DropdownMenuLabel>
        </DropdownMenuGroup>
>>>>>>> 76704d7 (feat: add AI workspace, authentication, collections, and platform infrastructure)

        <DropdownMenuSeparator className="bg-border" />

        <div className="px-2 py-1.5">
          <p className="truncate text-xs font-medium text-text-secondary">
            {data.organization.name}
          </p>
          <p className="text-xs text-text-muted capitalize">{data.role}</p>
        </div>

        <DropdownMenuSeparator className="bg-border" />

        <DropdownMenuItem
          onClick={handleLogout}
          className="px-2 py-1.5 text-sm text-critical focus:bg-critical/10 focus:text-critical"
        >
          <LogOut size={14} strokeWidth={1.75} className="mr-1.5" />
          Sign out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
