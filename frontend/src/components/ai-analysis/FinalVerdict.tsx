"use client";

import { motion } from "framer-motion";
import type { TransitionAnalysis } from "@/types/transition-analysis";

interface FinalVerdictProps {
  analysis: TransitionAnalysis;
  visible: boolean;
  onReplay: () => void;
}

export function FinalVerdict({
  analysis,
  visible,
  onReplay,
}: FinalVerdictProps) {
  if (!visible) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="rounded-lg border border-zinc-800 bg-zinc-900/30 px-5 py-5"
    >
      <div className="flex flex-col items-center gap-3 text-center">
        <span className="text-lg tracking-wide text-amber-400">
          {"★".repeat(5)}
        </span>

        <div>
          <p className="text-base font-semibold text-white">
            Excellent Harmonic Transition
          </p>
          <p className="mt-0.5 text-[12px] text-zinc-500">
            {analysis.overallScore} / 10 · {analysis.aiConfidence}% Confidence
          </p>
        </div>

        <p className="max-w-md text-[12px] leading-relaxed text-zinc-400">
          The AI concluded that the transition preserved energy, maintained
          harmonic compatibility, and executed the bass transfer at the ideal
          moment — the beginning of a new phrase.
        </p>

        <motion.button
          onClick={onReplay}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="mt-1 inline-flex h-9 items-center gap-1.5 rounded-lg border border-zinc-700 bg-zinc-800/50 px-4 text-[11px] font-medium text-zinc-300 transition-colors hover:border-zinc-600 hover:text-white"
        >
          <svg
            width="13"
            height="13"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <polygon points="5,3 19,12 5,21" />
          </svg>
          Replay Analysis
        </motion.button>
      </div>
    </motion.div>
  );
}
