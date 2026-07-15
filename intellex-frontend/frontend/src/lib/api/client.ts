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

    return Promise.reject(new ApiError(message, status));
  }
);
