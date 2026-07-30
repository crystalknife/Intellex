import { apiClient } from "@/lib/api/client";
import type { OrganizationInvite, OrganizationMember, OrganizationRole } from "@/lib/types";

interface RawMember {
  user_id: string;
  email: string;
  full_name: string;
  role: OrganizationRole;
  joined_at: string;
}

interface RawInvite {
  id: string;
  email: string;
  role: OrganizationRole;
  token: string;
  created_at: string;
  expires_at: string;
}

function toMember(raw: RawMember): OrganizationMember {
  return {
    userId: raw.user_id,
    email: raw.email,
    fullName: raw.full_name,
    role: raw.role,
    joinedAt: raw.joined_at,
  };
}

function toInvite(raw: RawInvite): OrganizationInvite {
  return {
    id: raw.id,
    email: raw.email,
    role: raw.role,
    token: raw.token,
    createdAt: raw.created_at,
    expiresAt: raw.expires_at,
  };
}

export async function getMembers(): Promise<OrganizationMember[]> {
  const { data } = await apiClient.get<{ items: RawMember[] }>(
    "/organization/members"
  );

  return data.items.map(toMember);
}

export async function updateMemberRole(
  userId: string,
  role: OrganizationRole
): Promise<OrganizationMember> {
  const { data } = await apiClient.patch<RawMember>(
    `/organization/members/${userId}`,
    { role }
  );

  return toMember(data);
}

export async function removeMember(userId: string): Promise<void> {
  await apiClient.delete(`/organization/members/${userId}`);
}

export async function getInvites(): Promise<OrganizationInvite[]> {
  const { data } = await apiClient.get<{ items: RawInvite[] }>(
    "/organization/invites"
  );

  return data.items.map(toInvite);
}

export async function createInvite(
  email: string,
  role: OrganizationRole = "member"
): Promise<OrganizationInvite> {
  const { data } = await apiClient.post<RawInvite>("/organization/invites", {
    email,
    role,
  });

  return toInvite(data);
}

export async function revokeInvite(id: string): Promise<void> {
  await apiClient.delete(`/organization/invites/${id}`);
}
