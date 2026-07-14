/**
 * Typed access to environment variables. Import this instead of reading
 * `process.env` directly so a missing/misspelled var fails loudly in one
 * place instead of silently producing `undefined` deep in a component.
 */

function readEnv(name: string, fallback?: string): string {
  const value = process.env[name] ?? fallback;

  if (value === undefined) {
    throw new Error(`Missing required environment variable: ${name}`);
  }

  return value;
}

export const env = {
  API_URL: readEnv("NEXT_PUBLIC_API_URL", "http://127.0.0.1:8000"),
};
