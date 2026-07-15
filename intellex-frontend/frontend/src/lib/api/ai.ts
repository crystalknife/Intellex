import { apiClient } from "@/lib/api/client";
import type { AISource, AIStatus } from "@/lib/types";

export async function getAIStatus(): Promise<AIStatus> {
  const { data } = await apiClient.get<{ configured: boolean; model: string }>(
    "/ai/status"
  );

  return data;
}

export interface AskAIParams {
  question: string;
  history?: Array<{ role: "user" | "assistant"; content: string }>;
}

export interface AskAIResult {
  answer: string;
  sources: AISource[];
  model: string;
}

export async function askAI(params: AskAIParams): Promise<AskAIResult> {
  const { data } = await apiClient.post<AskAIResult>(
    "/ai/chat",
    {
      question: params.question,
      history: params.history ?? [],
    },
    { timeout: 45_000 }
  );

  return data;
}
