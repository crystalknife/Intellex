"use client";

import { AlertCircle, ArrowRight, Hexagon } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { useSignup } from "@/hooks/useAuth";
import { ApiError } from "@/lib/api";
import { ROUTES } from "@/lib/constants";

export default function SignupPage() {
  const router = useRouter();
  const signup = useSignup();

  const [fullName, setFullName] = useState("");
  const [organizationName, setOrganizationName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const canSubmit =
    email.trim() && password.length >= 8 && organizationName.trim();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    signup.mutate(
      {
        email: email.trim(),
        password,
        fullName: fullName.trim(),
        organizationName: organizationName.trim(),
      },
      {
        onSuccess: () => router.push(ROUTES.intelligence),
        onError: (err) => {
          setError(
            err instanceof ApiError ? err.message : "Something went wrong."
          );
        },
      }
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-base px-4 py-10">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex items-center justify-center gap-2">
          <Hexagon
            size={24}
            strokeWidth={2}
            className="text-accent"
            fill="var(--color-accent-dim)"
          />
          <span className="text-lg font-semibold tracking-tight text-text-primary">
            Intellex
          </span>
        </div>

        <div className="rounded-(--radius-lg) border border-border bg-glass-1 p-6">
          <h1 className="mb-1 text-base font-medium text-text-primary">
            Create your workspace
          </h1>
          <p className="mb-6 text-sm text-text-secondary">
            You&rsquo;ll be the owner of a new organization.
          </p>

          <form onSubmit={handleSubmit} className="flex flex-col gap-3">
            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-text-secondary">
                Organization name
              </span>
              <input
                required
                value={organizationName}
                onChange={(e) => setOrganizationName(e.target.value)}
                placeholder="Acme Inc"
                className="focus-ring rounded-(--radius-md) border border-border bg-glass-2 px-3 py-2 text-sm text-text-primary placeholder:text-text-muted"
              />
            </label>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-text-secondary">
                Your name
              </span>
              <input
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Jane Doe"
                className="focus-ring rounded-(--radius-md) border border-border bg-glass-2 px-3 py-2 text-sm text-text-primary placeholder:text-text-muted"
              />
            </label>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-text-secondary">
                Email
              </span>
              <input
                type="email"
                required
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                className="focus-ring rounded-(--radius-md) border border-border bg-glass-2 px-3 py-2 text-sm text-text-primary placeholder:text-text-muted"
              />
            </label>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-text-secondary">
                Password
              </span>
              <input
                type="password"
                required
                autoComplete="new-password"
                minLength={8}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="At least 8 characters"
                className="focus-ring rounded-(--radius-md) border border-border bg-glass-2 px-3 py-2 text-sm text-text-primary placeholder:text-text-muted"
              />
            </label>

            {error && (
              <div className="flex items-start gap-2 rounded-(--radius-md) border border-critical/30 bg-critical/10 px-3 py-2 text-xs text-critical">
                <AlertCircle
                  size={14}
                  strokeWidth={1.75}
                  className="mt-0.5 shrink-0"
                />
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={signup.isPending || !canSubmit}
              className="focus-ring mt-1 flex items-center justify-center gap-1.5 rounded-(--radius-md) border border-accent/40 bg-accent-dim px-3 py-2 text-sm font-medium text-text-accent transition-colors duration-(--dur-fast) hover:bg-accent-glow disabled:cursor-not-allowed disabled:opacity-50"
            >
              {signup.isPending ? "Creating workspace..." : "Create workspace"}
              {!signup.isPending && (
                <ArrowRight size={14} strokeWidth={1.75} />
              )}
            </button>
          </form>
        </div>

        <p className="mt-4 text-center text-sm text-text-muted">
          Already have an account?{" "}
          <Link
            href={ROUTES.login}
            className="focus-ring rounded-(--radius-sm) text-text-accent hover:underline"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
