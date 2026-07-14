/**
 * Structured logger. The interface here is intentionally small and
 * stable -- it can be backed by console today and swapped for
 * Sentry/OpenTelemetry/Axiom later without touching call sites.
 */

type LogContext = Record<string, unknown> | undefined;

function format(level: string, message: string, context?: LogContext) {
  return context
    ? [`[Intellex:${level}] ${message}`, context]
    : [`[Intellex:${level}] ${message}`];
}

export const logger = {
  info(message: string, context?: LogContext) {
    if (process.env.NODE_ENV !== "production") {
      console.log(...format("info", message, context));
    }
  },
  warn(message: string, context?: LogContext) {
    console.warn(...format("warn", message, context));
  },
  error(message: string, error?: unknown, context?: LogContext) {
    console.error(...format("error", message, context), error ?? "");
  },
  debug(message: string, context?: LogContext) {
    if (process.env.NODE_ENV !== "production") {
      console.debug(...format("debug", message, context));
    }
  },
};
