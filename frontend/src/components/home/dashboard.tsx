"use client";

import { motion } from "framer-motion";
import type { UploadAnalysisResponse } from "@/types";

import { AIRecommendationCard } from "@/components/ai/AIRecommendationCard";
import { MixMindScoreCard } from "@/components/ai/MixMindScoreCard";
import { WhyThisScore } from "@/components/ai/WhyThisScore";
import { TransitionTimeline } from "@/components/ai/TransitionTimeline";
import { RadarChartCard } from "@/components/ai/RadarChart";
import { HeatIndicators } from "@/components/ai/HeatIndicators";
import { DJExecutionTimeline } from "@/components/ai/DJExecutionTimeline";
import { CompatibilityCard } from "./compatibility-card";
import { TrackCard } from "./track-card";

interface DashboardProps {
  result: UploadAnalysisResponse;
}

export function Dashboard({ result }: DashboardProps) {
  const waveforms = result.waveforms;
  const spectrograms = result.spectrograms;

  if (!waveforms || !spectrograms) {
    return null;
  }

  const r = result.ai_recommendation;
  const compat = result.compatibility;

  return (
    <motion.section
      className="w-full"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
    >
      <div className="mx-auto w-full max-w-[1300px] px-4 md:px-6 lg:px-8">
        <div className="mt-10 flex flex-col gap-8">
          <MixMindScoreCard recommendation={r} compatibility={compat} />
          <WhyThisScore compatibility={compat} />

          <TrackCard
            title="Track A"
            analysis={result.track_a}
            waveform={waveforms.track_a}
            spectrogram={spectrograms.track_a}
          />

          <TrackCard
            title="Track B"
            analysis={result.track_b}
            waveform={waveforms.track_b}
            spectrogram={spectrograms.track_b}
          />

          <RadarChartCard recommendation={r} compatibility={compat} />

          <HeatIndicators recommendation={r} compatibility={compat} />

          <TransitionTimeline
            transitionType={r.transition_type}
            transitionQuality={r.transition_quality}
            transitionLength={r.recommended_transition_length}
          />

          <CompatibilityCard compatibility={compat} />

          <AIRecommendationCard recommendation={r} />

          <DJExecutionTimeline execution={r.dj_execution} />
        </div>
      </div>
    </motion.section>
  );
}
