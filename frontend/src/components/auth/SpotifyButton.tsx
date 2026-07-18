"use client";

import { forwardRef } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface SpotifyButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
}

const SpotifyButton = forwardRef<HTMLButtonElement, SpotifyButtonProps>(
  ({ className, loading, disabled, children, onClick, ...props }, ref) => {
    return (
      <motion.div
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.99 }}
        className={cn(
          "group relative w-full overflow-hidden rounded-xl border border-border/50 bg-card/50",
          "hover:border-[#1DB954]/30 hover:bg-card-hover hover:shadow-lg hover:shadow-[#1DB954]/5",
          "focus-within:ring-2 focus-within:ring-[#1DB954]/50 focus-within:ring-offset-2 focus-within:ring-offset-background",
          "disabled:pointer-events-none disabled:opacity-50",
          loading && "cursor-wait"
        )}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-[#1DB954]/0 via-[#1DB954]/[0.03] to-[#1DB954]/0 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
        <button
          ref={ref}
          disabled={disabled || loading}
          onClick={onClick}
          className={cn("flex w-full items-center justify-center gap-3 px-4 py-3 text-sm font-medium text-text focus-visible:outline-none disabled:pointer-events-none", className)}
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
            <svg className="h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="#1DB954" aria-hidden="true">
              <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z" />
            </svg>
          )}
          <span className="relative z-10">{loading ? "Redirecting..." : children || "Continue with Spotify"}</span>
        </button>
      </motion.div>
    );
  }
);
SpotifyButton.displayName = "SpotifyButton";

export { SpotifyButton };
