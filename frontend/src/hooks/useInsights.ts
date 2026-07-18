"use client";

import { useMemo, useRef } from "react";
import type { AIInsight, DemoMetadata } from "@/types/video";

interface UseInsightsOptions {
  currentTime: number;
  metadata?: DemoMetadata;
}

export function useInsights({ currentTime, metadata }: UseInsightsOptions) {
  const historyRef = useRef<AIInsight[]>([]);

  const insights = useMemo(() => metadata?.insights ?? [], [metadata]);

  const currentInsight = useMemo(() => {
    const match = insights.find((insight) => {
      const end = insight.time + insight.duration;
      return currentTime >= insight.time && currentTime < end;
    }) ?? null;
    if (match && !historyRef.current.find((h) => h.time === match.time)) {
      historyRef.current = [...historyRef.current, match];
    }
    return match;
  }, [insights, currentTime]);

  const nextInsight = useMemo(() => {
    const upcoming = insights
      .filter((insight) => insight.time > currentTime)
      .sort((a, b) => a.time - b.time);
    return upcoming[0] ?? null;
  }, [insights, currentTime]);

  const timeToNextInsight = useMemo(() => {
    if (!nextInsight) return null;
    return Math.max(0, nextInsight.time - currentTime);
  }, [nextInsight, currentTime]);

  return {
    currentInsight,
    insightHistory: historyRef.current,
    nextInsight,
    timeToNextInsight,
  };
}
