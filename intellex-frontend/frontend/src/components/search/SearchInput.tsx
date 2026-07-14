"use client";

import { Search } from "lucide-react";
import { forwardRef } from "react";

import { cn } from "@/lib/utils";

interface SearchInputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

export const SearchInput = forwardRef<HTMLInputElement, SearchInputProps>(
  function SearchInput({ className, ...props }, ref) {
    return (
      <div className="flex items-center gap-2.5 border-b border-border px-4 py-3">
        <Search size={16} strokeWidth={1.75} className="shrink-0 text-text-muted" />
        <input
          ref={ref}
          type="text"
          className={cn(
            "w-full bg-transparent text-[15px] text-text-primary placeholder:text-text-muted focus:outline-none",
            className
          )}
          {...props}
        />
      </div>
    );
  }
);
