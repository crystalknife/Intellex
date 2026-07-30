"use client";

import { AlertCircle, ArrowUp, Sparkles } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { MarkdownMessage } from "@/components/ai/markdown-message";
import { useAIStatus, useAskAI } from "@/hooks/useAI";
import { ApiError } from "@/lib/api";
import type { AIChatMessage } from "@/lib/types";
import { cn } from "@/lib/utils";

export default function AIWorkspacePage() {
  const { data: status, isLoading: statusLoading } = useAIStatus();
  const askAI = useAskAI();
  const router = useRouter();
  const searchParams = useSearchParams();

  const [messages, setMessages] = useState<AIChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const autoAskedRef = useRef(false);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, askAI.isPending]);

  // Deep-link support: CommandPalette's "Ask Intellex about X" row routes
  // here as /ai?q=<query>. Auto-fire that question once, on first load,
  // then strip the param so a manual refresh/back-nav doesn't re-ask it.
  useEffect(() => {
    if (autoAskedRef.current) return;
    if (statusLoading || !status?.configured) return;

    const q = searchParams.get("q")?.trim();
    if (!q) return;

    autoAskedRef.current = true;
    router.replace("/ai");
    askQuestion(q);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusLoading, status?.configured, searchParams]);

  function askQuestion(question: string) {
    if (!question || askAI.isPending) return;

    setError(null);
    const nextMessages: AIChatMessage[] = [
      ...messages,
      { role: "user", content: question },
    ];
    setMessages(nextMessages);
    setInput("");

    askAI.mutate(
      {
        question,
        history: messages.map((m) => ({ role: m.role, content: m.content })),
      },
      {
        onSuccess: (result) => {
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: result.answer,
              sources: result.sources,
            },
          ]);
        },
        onError: (err) => {
          setError(
            err instanceof ApiError
              ? err.message
              : "Something went wrong asking the AI."
          );
        },
      }
    );
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    askQuestion(input.trim());
  }

  if (statusLoading) {
    return (
      <div className="mx-auto flex max-w-3xl flex-col gap-4 px-4 py-6 lg:px-8 lg:py-8">
        <Skeleton className="h-7 w-1/3" />
        <Skeleton className="h-48 w-full rounded-(--radius-lg)" />
      </div>
    );
  }

  if (!status?.configured) {
    return (
      <div className="mx-auto flex max-w-2xl flex-col gap-6 px-4 py-6 lg:px-8 lg:py-8">
        <div>
          <h1 className="text-lg font-medium text-text-primary">
            AI Workspace
          </h1>
          <p className="text-sm text-text-secondary">
            Ask questions about your document corpus.
          </p>
        </div>

        <EmptyState
          icon={Sparkles}
          title="AI Workspace isn't configured yet"
          description="Add an OpenRouter API key to backend/.env to enable this. It's free -- OpenRouter has several no-cost models, and Intellex automatically falls back across whichever ones you configure."
        />

        <div className="rounded-(--radius-lg) border border-border bg-glass-1 p-4 font-mono text-xs text-text-secondary">
          <p className="mb-2 text-text-muted"># backend/.env</p>
          <p>OPENROUTER_API_KEY=sk-or-v1-...</p>
          <p>OPENROUTER_MODELS=google/gemma-4-31b-it:free,openrouter/free</p>
        </div>

        <p className="text-xs text-text-muted">
          Restart the backend after adding the key.
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto flex h-full max-w-3xl flex-col px-4 py-6 lg:px-8 lg:py-8">
      <div className="mb-4">
        <h1 className="text-lg font-medium text-text-primary">
          AI Workspace
        </h1>
        <p className="text-sm text-text-secondary">
          Answers are grounded in your ingested documents, via{" "}
          <span className="text-text-accent">{status.model}</span>.
        </p>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto pb-4">
        {messages.length === 0 && (
          <EmptyState
            icon={Sparkles}
            title="Ask about what's happening"
            description={`Try "What's the latest on NVIDIA?" or "Summarize today's biggest story."`}
          />
        )}

        {messages.map((message, i) => (
          <div
            key={i}
            className={cn(
              "flex flex-col gap-2 rounded-(--radius-lg) px-4 py-3 text-sm leading-relaxed",
              message.role === "user"
                ? "ml-auto max-w-[85%] bg-accent-dim text-text-primary"
                : "mr-auto max-w-[85%] border border-border bg-glass-1 text-text-primary"
            )}
          >
            {message.role === "assistant" ? (
              <MarkdownMessage content={message.content} sources={message.sources} />
            ) : (
              <p className="whitespace-pre-wrap">{message.content}</p>
            )}

            {message.sources && message.sources.length > 0 && (
              <div className="flex flex-wrap gap-1.5 border-t border-border pt-2">
                {message.sources.map((source, idx) => (
                  <a
                    key={source.id}
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="focus-ring rounded-(--radius-sm) border border-border-mid bg-glass-2 px-2 py-1 text-xs text-text-secondary transition-colors duration-(--dur-fast) hover:text-text-primary"
                  >
                    [{idx + 1}] {source.source}
                  </a>
                ))}
              </div>
            )}
          </div>
        ))}

        {askAI.isPending && (
          <div className="mr-auto flex max-w-[85%] items-center gap-2 rounded-(--radius-lg) border border-border bg-glass-1 px-4 py-3 text-sm text-text-muted">
            <span className="flex gap-1">
              <span className="size-1.5 animate-pulse rounded-full bg-text-muted [animation-delay:0ms]" />
              <span className="size-1.5 animate-pulse rounded-full bg-text-muted [animation-delay:150ms]" />
              <span className="size-1.5 animate-pulse rounded-full bg-text-muted [animation-delay:300ms]" />
            </span>
            Thinking...
          </div>
        )}

        {error && (
          <div className="mr-auto flex max-w-[85%] items-start gap-2 rounded-(--radius-lg) border border-critical/30 bg-critical/10 px-4 py-3 text-sm text-critical">
            <AlertCircle size={14} strokeWidth={1.75} className="mt-0.5 shrink-0" />
            {error}
          </div>
        )}

        <div ref={scrollRef} />
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2 border-t border-border pt-4">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your documents..."
          disabled={askAI.isPending}
          className="focus-ring w-full rounded-(--radius-md) border border-border bg-glass-1 px-3 py-2 text-sm text-text-primary placeholder:text-text-muted disabled:opacity-60"
        />
        <button
          type="submit"
          disabled={!input.trim() || askAI.isPending}
          aria-label="Send"
          className="focus-ring flex shrink-0 items-center justify-center rounded-(--radius-md) border border-accent/40 bg-accent-dim px-3 py-2 text-text-accent transition-colors duration-(--dur-fast) hover:bg-accent-glow disabled:cursor-not-allowed disabled:opacity-50"
        >
          <ArrowUp size={16} strokeWidth={1.75} />
        </button>
      </form>
    </div>
  );
}
