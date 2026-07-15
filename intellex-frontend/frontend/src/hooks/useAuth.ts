"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  clearStoredToken,
  getMe,
  getStoredToken,
  login,
  setStoredToken,
  signup,
  type LoginParams,
  type SignupParams,
} from "@/lib/api/auth";
import { QUERY_KEYS } from "@/lib/constants";
import type { AuthSession } from "@/lib/types";

function persistSession(session: AuthSession) {
  setStoredToken(session.accessToken);
}

export function useSignup() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (params: SignupParams) => signup(params),
    onSuccess: (session) => {
      persistSession(session);
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.currentUser() });
    },
  });
}

export function useLogin() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (params: LoginParams) => login(params),
    onSuccess: (session) => {
      persistSession(session);
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.currentUser() });
    },
  });
}

export function useLogout() {
  const queryClient = useQueryClient();

  return () => {
    clearStoredToken();
    queryClient.invalidateQueries({ queryKey: QUERY_KEYS.currentUser() });
    queryClient.setQueryData(QUERY_KEYS.currentUser(), null);
  };
}

/**
 * Current user, derived from a valid stored token. `enabled` is gated on
 * a token actually being present so this doesn't fire (and log a 401)
 * on every page load for a signed-out visitor -- Phase A has no
 * route-level gating yet, so plenty of pages render without anyone
 * ever calling this.
 */
export function useCurrentUser() {
  return useQuery({
    queryKey: QUERY_KEYS.currentUser(),
    queryFn: getMe,
    enabled: Boolean(getStoredToken()),
    retry: false,
    staleTime: 5 * 60_000,
  });
}
