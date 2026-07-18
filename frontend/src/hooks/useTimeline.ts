"use client";

import { useMemo } from "react";
import type { DemoMetadata } from "@/types/video";

interface UseTimelineOptions {
  currentTime: number;
  duration: number;
  metadata?: DemoMetadata;
}

export function useTimeline({ currentTime, duration, metadata }: UseTimelineOptions) {
  const chapters = useMemo(() => metadata?.chapters ?? [], [metadata]);
  const markers = useMemo(() => metadata?.markers ?? [], [metadata]);
  const transitionZones = useMemo(() => metadata?.transitionZones ?? [], [metadata]);
  const trackA = metadata?.tracks.a;
  const trackB = metadata?.tracks.b;

  const progress = useMemo(() => {
    if (duration <= 0) return 0;
    return Math.min(currentTime / duration, 1);
  }, [currentTime, duration]);

  const currentChapter = useMemo(() => {
    if (chapters.length === 0) return null;
    let active = chapters[0];
    for (const ch of chapters) {
      if (ch.time <= currentTime) {
        active = ch;
      }
    }
    return active;
  }, [chapters, currentTime]);

  const nextMarker = useMemo(() => {
    return markers.find((m) => m.time > currentTime) ?? null;
  }, [markers, currentTime]);

  const currentPhase = useMemo((): "track-a" | "blending" | "track-b" => {
    if (!transitionZones.length) return "track-a";
    const inZone = transitionZones.find(
      (z) => currentTime >= z.startTime && currentTime <= z.endTime,
    );
    if (inZone) return "blending";
    const lastZoneEnd = transitionZones[transitionZones.length - 1]?.endTime ?? 0;
    return currentTime >= lastZoneEnd ? "track-b" : "track-a";
  }, [transitionZones, currentTime]);

  const activeZones = useMemo(() => {
    return transitionZones.filter(
      (z) => currentTime >= z.startTime && currentTime <= z.endTime,
    );
  }, [transitionZones, currentTime]);

  const upcomingZones = useMemo(() => {
    return transitionZones.filter((z) => z.startTime > currentTime);
  }, [transitionZones, currentTime]);

  return {
    chapters,
    markers,
    transitionZones,
    trackA,
    trackB,
    progress,
    currentChapter,
    nextMarker,
    currentPhase,
    activeZones,
    upcomingZones,
  };
}
