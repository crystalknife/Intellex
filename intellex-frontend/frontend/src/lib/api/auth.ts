import { apiClient } from "@/lib/api/client";
import type { AuthSession, CurrentUser, Organization, User } from "@/lib/types";

const TOKEN_STORAGE_KEY = "intellex.auth.token";

interface RawUser {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
}

interface RawOrganization {
  id: string;
  name: string;
  created_at: string;
}

interface RawAuthSession {
  access_token: string;
  token_type: string;
  user: RawUser;
  organization: RawOrganization;
  role: "owner" | "admin" | "member";
}

interface RawCurrentUser {
  user: RawUser;
  organization: RawOrganization;
  role: "owner" | "admin" | "member";
}

function toUser(raw: RawUser): User {
  return {
    id: raw.id,
    email: raw.email,
    fullName: raw.full_name,
    createdAt: raw.created_at,
  };
}

function toOrganization(raw: RawOrganization): Organization {
  return {
    id: raw.id,
    name: raw.name,
    createdAt: raw.created_at,
  };
}

function toSession(raw: RawAuthSession): AuthSession {
  return {
    accessToken: raw.access_token,
    tokenType: raw.token_type,
    user: toUser(raw.user),
    organization: toOrganization(raw.organization),
    role: raw.role,
  };
}

export interface SignupParams {
  email: string;
  password: string;
  fullName?: string;
  organizationName: string;
}

export interface LoginParams {
  email: string;
  password: string;
}

export async function signup(params: SignupParams): Promise<AuthSession> {
  const { data } = await apiClient.post<RawAuthSession>("/auth/signup", {
    email: params.email,
    password: params.password,
    full_name: params.fullName ?? "",
    organization_name: params.organizationName,
  });

  return toSession(data);
}

export async function login(params: LoginParams): Promise<AuthSession> {
  const { data } = await apiClient.post<RawAuthSession>("/auth/login", {
    email: params.email,
    password: params.password,
  });

  return toSession(data);
}

export async function getMe(): Promise<CurrentUser> {
  const { data } = await apiClient.get<RawCurrentUser>("/auth/me");

  return {
    user: toUser(data.user),
    organization: toOrganization(data.organization),
    role: data.role,
  };
}

/**
 * Token storage. Plain localStorage, not cookies -- the frontend and API
 * are already different origins in dev (see settings.py's CORS_ORIGINS),
 * and JWT was chosen specifically to sidestep cross-origin cookie
 * friction. Guarded for SSR since these run during Next.js server
 * rendering where `window` doesn't exist.
 */

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;

  return window.localStorage.getItem(TOKEN_STORAGE_KEY);
}

export function setStoredToken(token: string): void {
  if (typeof window === "undefined") return;

  window.localStorage.setItem(TOKEN_STORAGE_KEY, token);
}

export function clearStoredToken(): void {
  if (typeof window === "undefined") return;

  window.localStorage.removeItem(TOKEN_STORAGE_KEY);
}
