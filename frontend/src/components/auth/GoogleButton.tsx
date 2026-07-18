"use client";

import { forwardRef } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface GoogleButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
}

const GoogleButton = forwardRef<HTMLButtonElement, GoogleButtonProps>(
  ({ className, loading, disabled, children, onClick, ...props }, ref) => {
    return (
      <motion.div
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.99 }}
        className={cn(
          "group relative w-full overflow-hidden rounded-xl border border-border/50 bg-card/50",
          "hover:border-border-light hover:bg-card-hover hover:shadow-lg hover:shadow-primary/5",
          "focus-within:ring-2 focus-within:ring-primary/50 focus-within:ring-offset-2 focus-within:ring-offset-background",
          "disabled:pointer-events-none disabled:opacity-50",
          loading && "cursor-wait"
        )}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-primary/0 via-primary/[0.03] to-primary/0 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
        <button
          ref={ref}
          disabled={disabled || loading}
          onClick={onClick}
          className="flex w-full items-center justify-center gap-3 px-4 py-3 text-sm font-medium text-text focus-visible:outline-none disabled:pointer-events-none"
          {...props}
        >
          {loading ? (
            <svg
              className="h-5 w-5 animate-spin text-text-secondary"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          ) : (
            <svg className="h-5 w-5 shrink-0" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4" />
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
            </svg>
          )}
          <span className="relative z-10">{loading ? "Redirecting..." : children || "Continue with Google"}</span>
        </button>
      </motion.div>
    );
  }
);
GoogleButton.displayName = "GoogleButton";

export { GoogleButton };
