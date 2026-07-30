"use client";

import { Check, Copy } from "lucide-react";
import { useState } from "react";
import ReactMarkdown, { defaultUrlTransform, type Components } from "react-markdown";
import remarkGfm from "remark-gfm";

import { cn } from "@/lib/utils";
import type { AISource } from "@/lib/types";

/**
 * Turns bare numeric citation markers ("...as reported [1].") into
 * markdown links on a private `citation:` scheme, so ReactMarkdown's
 * own link-rendering pipeline can be reused to turn them into clickable
 * pills (see the `a` override below) instead of writing a custom remark
 * plugin for the same result.
 *
 * This only changes how the *existing* citation markers are displayed
 * -- it doesn't change whether/how the model produces them (that's the
 * system prompt in backend/app/ai/service.py, untouched) and it doesn't
 * touch the separately-rendered source list either. The regex matches
 * only brackets containing purely digits, so it can't misfire on a
 * genuine markdown link like "[Read the article](url)".
 */
function linkifyCitations(content: string): string {
  return content.replace(/\[(\d+)\]/g, (match, num) => `[${match}](citation:${num})`);
}

/**
 * react-markdown sanitizes link URLs by default (blocks javascript:,
 * data:, and anything else not on its protocol allowlist -- a real
 * XSS protection since `content` here is model output, not trusted
 * text). The private `citation:` scheme from linkifyCitations() above
 * would get silently blanked by that same sanitizer, so this adds
 * exactly one allowlisted exception for it and defers to the library's
 * own defaultUrlTransform for every other URL, preserving its original
 * protection for genuine links the model writes.
 */
function urlTransform(url: string): string {
  return url.startsWith("citation:") ? url : defaultUrlTransform(url);
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // Clipboard access can fail (permissions, insecure context) --
      // silently no-op rather than surfacing an error for a
      // non-critical convenience action.
    }
  }

  return (
    <button
      onClick={handleCopy}
      aria-label={copied ? "Copied" : "Copy response"}
      className="focus-ring flex items-center gap-1 rounded-(--radius-sm) px-1.5 py-1 text-xs text-text-muted transition-colors duration-(--dur-fast) hover:bg-glass-2 hover:text-text-secondary"
    >
      {copied ? (
        <>
          <Check size={12} strokeWidth={1.75} />
          Copied
        </>
      ) : (
        <>
          <Copy size={12} strokeWidth={1.75} />
          Copy
        </>
      )}
    </button>
  );
}

export function MarkdownMessage({
  content,
  sources = [],
}: {
  content: string;
  sources?: AISource[];
}) {
  const components: Components = {
    p({ children }) {
      return <p className="mb-2 last:mb-0">{children}</p>;
    },
    h1({ children }) {
      return (
        <h3 className="mt-3 mb-1.5 text-base font-medium text-text-primary first:mt-0">
          {children}
        </h3>
      );
    },
    h2({ children }) {
      return (
        <h4 className="mt-3 mb-1.5 text-sm font-medium text-text-primary first:mt-0">
          {children}
        </h4>
      );
    },
    h3({ children }) {
      return (
        <h5 className="mt-2 mb-1 text-sm font-medium text-text-primary first:mt-0">
          {children}
        </h5>
      );
    },
    ul({ children }) {
      return <ul className="mb-2 list-disc space-y-1 pl-5 last:mb-0">{children}</ul>;
    },
    ol({ children }) {
      return <ol className="mb-2 list-decimal space-y-1 pl-5 last:mb-0">{children}</ol>;
    },
    li({ children }) {
      return <li className="leading-relaxed">{children}</li>;
    },
    strong({ children }) {
      return <strong className="font-semibold text-text-primary">{children}</strong>;
    },
    em({ children }) {
      return <em className="italic">{children}</em>;
    },
    blockquote({ children }) {
      return (
        <blockquote className="mb-2 border-l-2 border-border-mid pl-3 text-text-secondary last:mb-0">
          {children}
        </blockquote>
      );
    },
    hr() {
      return <hr className="my-3 border-border" />;
    },
    code({ className, children }) {
      const isBlock = /language-/.test(className ?? "");

      if (isBlock) {
        return (
          <code
            className={cn(
              "block overflow-x-auto rounded-(--radius-sm) bg-glass-2 p-2.5 font-mono text-xs text-text-primary",
              className
            )}
          >
            {children}
          </code>
        );
      }

      return (
        <code className="rounded-(--radius-xs) bg-glass-2 px-1 py-0.5 font-mono text-[0.85em] text-text-accent">
          {children}
        </code>
      );
    },
    pre({ children }) {
      return <pre className="mb-2 last:mb-0">{children}</pre>;
    },
    table({ children }) {
      return (
        <div className="mb-2 overflow-x-auto last:mb-0">
          <table className="w-full border-collapse text-xs">{children}</table>
        </div>
      );
    },
    th({ children }) {
      return (
        <th className="border-b border-border-mid px-2 py-1 text-left font-medium text-text-secondary">
          {children}
        </th>
      );
    },
    td({ children }) {
      return <td className="border-b border-border px-2 py-1">{children}</td>;
    },
    a({ href, children }) {
      if (href?.startsWith("citation:")) {
        const index = Number(href.slice("citation:".length));
        const source = sources[index - 1];

        if (!source) {
          // Model cited a number with no matching source -- render the
          // plain marker rather than a dead/misleading link.
          return <span className="text-text-muted">{children}</span>;
        }

        return (
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            title={source.title}
            className="focus-ring mx-0.5 inline-flex items-center rounded-(--radius-xs) bg-accent-dim px-1 align-super text-[0.7em] font-medium text-text-accent no-underline transition-colors duration-(--dur-fast) hover:bg-accent-glow"
          >
            {index}
          </a>
        );
      }

      return (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="text-text-accent underline underline-offset-2 hover:text-text-primary"
        >
          {children}
        </a>
      );
    },
  };

  return (
    <div className="group/message flex flex-col gap-1.5">
      <div className="text-sm leading-relaxed [&>*:last-child]:mb-0">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={components}
          urlTransform={urlTransform}
        >
          {linkifyCitations(content)}
        </ReactMarkdown>
      </div>

      <div className="opacity-0 transition-opacity duration-(--dur-fast) group-hover/message:opacity-100">
        <CopyButton text={content} />
      </div>
    </div>
  );
}
