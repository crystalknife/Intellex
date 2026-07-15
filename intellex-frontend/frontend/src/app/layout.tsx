import type { Metadata } from "next";
import { Geist_Mono, Inter } from "next/font/google";

import { AppShell } from "@/components/layout/app-shell";
import { RouteAwareShell } from "@/components/layout/route-aware-shell";
import { SkipToContent } from "@/components/layout/skip-to-content";
import { GlobalErrorBoundary } from "@/components/error/GlobalErrorBoundary";
import { Providers } from "@/providers";
import { APP_DESCRIPTION, APP_NAME } from "@/lib/constants";

import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: `${APP_NAME} \u2014 News Intelligence Operating System`,
  description: APP_DESCRIPTION,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`dark ${inter.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="flex h-full min-h-full flex-col bg-base text-text-primary">
        <SkipToContent />
        <GlobalErrorBoundary>
          <Providers>
            <RouteAwareShell shell={<AppShell>{children}</AppShell>}>
              {children}
            </RouteAwareShell>
          </Providers>
        </GlobalErrorBoundary>
      </body>
    </html>
  );
}
