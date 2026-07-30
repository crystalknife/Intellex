"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createInvite,
  getInvites,
  getMembers,
  removeMember,
  revokeInvite,
  updateMemberRole,
} from "@/lib/api";
import type { OrganizationRole } from "@/lib/types";

const MEMBERS_KEY = ["organization", "members"] as const;
const INVITES_KEY = ["organization", "invites"] as const;

export function useMembers() {
  return useQuery({
    queryKey: MEMBERS_KEY,
    queryFn: getMembers,
    staleTime: 30_000,
  });
}

export function useUpdateMemberRole() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, role }: { userId: string; role: OrganizationRole }) =>
      updateMemberRole(userId, role),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: MEMBERS_KEY });
    },
  });
}

export function useRemoveMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (userId: string) => removeMember(userId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: MEMBERS_KEY });
    },
  });
}

export function useInvites() {
  return useQuery({
    queryKey: INVITES_KEY,
    queryFn: getInvites,
    staleTime: 30_000,
  });
}

export function useCreateInvite() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ email, role }: { email: string; role?: OrganizationRole }) =>
      createInvite(email, role),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: INVITES_KEY });
    },
  });
}

export function useRevokeInvite() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => revokeInvite(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: INVITES_KEY });
    },
  });
}
