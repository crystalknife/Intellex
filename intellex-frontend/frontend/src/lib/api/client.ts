import axios, { AxiosError } from "axios";

import { env } from "@/lib/env";
import { logger } from "@/lib/logger";

export const apiClient = axios.create({
  baseURL: env.API_URL,
  timeout: 10_000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Deliberately reads localStorage directly on each request (rather than
// importing getStoredToken from lib/api/auth) to avoid a circular
// import -- auth.ts imports this client, so this client can't import
// back from auth.ts.
const TOKEN_STORAGE_KEY = "intellex.auth.token";

apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = window.localStorage.getItem(TOKEN_STORAGE_KEY);

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }

  return config;
});

export class ApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const status = error.response?.status;
    const message =
      (error.response?.data as { detail?: string } | undefined)?.detail ??
      error.message ??
      "Request failed";

    logger.error("API request failed", error, {
      url: error.config?.url,
      status,
    });

    // Distinguish "my session expired" from "I typed the wrong password
    // on the login form" -- both are 401s, but only the former means
    // the stored token is stale and should be cleared. A request that
    // never carried an Authorization header (login/signup attempts)
    // failing with 401 is just a normal credentials error the calling
    // page already handles inline; redirecting on that would hijack
    // the login page's own error message.
    const hadToken = Boolean(error.config?.headers?.Authorization);
    const onAuthPage =
      typeof window !== "undefined" &&
      (window.location.pathname.startsWith("/login") ||
        window.location.pathname.startsWith("/signup"));

    if (status === 401 && hadToken && typeof window !== "undefined" && !onAuthPage) {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY);
      window.location.href = "/login";
    }

    return Promise.reject(new ApiError(message, status));
  }
);
