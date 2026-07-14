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
