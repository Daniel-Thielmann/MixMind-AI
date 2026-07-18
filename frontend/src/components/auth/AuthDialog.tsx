"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { GoogleButton } from "./GoogleButton";
import { GitHubButton } from "./GitHubButton";
import { SpotifyButton } from "./SpotifyButton";

interface AuthDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function AuthDialog({ open, onOpenChange }: AuthDialogProps) {
  const { signInGoogle, signInGithub, signInSpotify } = useAuth();
  const [loading, setLoading] = useState<"google" | "github" | "spotify" | null>(null);

  const signInFns = {
    google: signInGoogle,
    github: signInGithub,
    spotify: signInSpotify,
  } as const;

  const handleSignIn = async (provider: keyof typeof signInFns) => {
    setLoading(provider);
    try {
      await signInFns[provider]();
    } finally {
      setLoading(null);
    }
  };

  return (
    <AnimatePresence>
      {open && (
        <Dialog open={open} onOpenChange={onOpenChange}>
          <DialogContent className="sm:max-w-sm">
            <div className="flex flex-col items-center gap-6 py-4">
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
              >
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary-dark text-xl font-bold text-background shadow-lg shadow-primary/20">
                  M
                </div>
              </motion.div>

              <DialogHeader className="text-center">
                <DialogTitle className="text-xl">Continue to MixMind</DialogTitle>
                <DialogDescription className="text-balance pt-1">
                  Use your favorite provider to continue.
                </DialogDescription>
              </DialogHeader>

              <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.15, duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
                className="flex w-full flex-col gap-3"
              >
                <GoogleButton
                  loading={loading === "google"}
                  onClick={() => handleSignIn("google")}
                />
                <GitHubButton
                  loading={loading === "github"}
                  onClick={() => handleSignIn("github")}
                />
                <div className="relative my-1">
                  <div className="absolute inset-0 flex items-center">
                    <span className="w-full border-t border-border/50" />
                  </div>
                  <div className="relative flex justify-center text-xs">
                    <span className="bg-card/80 px-2 text-text-tertiary">Import your library</span>
                  </div>
                </div>
                <SpotifyButton
                  loading={loading === "spotify"}
                  onClick={() => handleSignIn("spotify")}
                />
              </motion.div>

              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.4 }}
                className="text-center text-xs text-text-tertiary"
              >
                By continuing, you agree to MixMind&apos;s{" "}
                <a href="#" className="underline underline-offset-2 hover:text-text-secondary transition-colors">
                  Terms
                </a>{" "}
                and{" "}
                <a href="#" className="underline underline-offset-2 hover:text-text-secondary transition-colors">
                  Privacy Policy
                </a>
                .
              </motion.p>
            </div>
          </DialogContent>
        </Dialog>
      )}
    </AnimatePresence>
  );
}
