"use client";

import { useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { TransitionAnalysis } from "@/types/transition-analysis";

interface LiveCommentaryProps {
  analysis: TransitionAnalysis;
  currentTime: number;
}

function formatTime(s: number): string {
  const m = Math.floor(s / 60);
  const sec = Math.floor(s % 60);
  return `${m.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
}

export function LiveCommentary({
  analysis,
  currentTime,
}: LiveCommentaryProps) {
  const currentEvent = useMemo(() => {
    const tolerance = 2;
    const active = analysis.events.find(
      (e) => Math.abs(currentTime - e.time) <= tolerance,
    );
    if (active) return active;

    const past = [...analysis.events]
      .reverse()
      .find((e) => currentTime >= e.time + tolerance);
    return past ?? null;
  }, [currentTime, analysis.events]);

  return (
    <div className="space-y-3">
      <p className="text-[11px] font-medium text-zinc-400">Live Commentary</p>
      <div className="relative min-h-[72px]">
        <AnimatePresence mode="wait">
          {currentEvent ? (
            <motion.div
              key={currentEvent.time}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.25 }}
              className="absolute inset-0"
            >
              <div className="rounded-lg border border-zinc-800 bg-zinc-900/40 px-4 py-3">
                <span className="font-mono text-[11px] font-medium text-primary">
                  {formatTime(currentEvent.time)}
                </span>
                <p className="mt-1 text-[13px] leading-relaxed text-zinc-300">
                  {currentEvent.description}
                </p>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="waiting"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="absolute inset-0 flex items-center justify-center rounded-lg border border-dashed border-zinc-800"
            >
              <span className="text-[12px] text-zinc-600">
                Waiting for transition start...
              </span>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
