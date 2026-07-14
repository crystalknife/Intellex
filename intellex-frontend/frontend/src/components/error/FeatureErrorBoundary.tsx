"use client";

import { AlertTriangle } from "lucide-react";
import { Component, type ReactNode } from "react";

import { logger } from "@/lib/logger";

import { EmptyState } from "@/components/ui/empty-state";

interface Props {
  name: string;
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

/**
 * Wraps a single workspace feature (brief, pipeline status, event grid,
 * feed) so a failure in one section never takes down the rest of the
 * page.
 */
export class FeatureErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    logger.error(`Feature "${this.props.name}" failed to render`, error, {
      componentStack: info.componentStack,
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <EmptyState
          icon={AlertTriangle}
          title="This section couldn't load"
          description="The rest of the workspace is unaffected."
        />
      );
    }

    return this.props.children;
  }
}
