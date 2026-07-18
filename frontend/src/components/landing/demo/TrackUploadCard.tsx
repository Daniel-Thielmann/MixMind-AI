"use client";

import { useState, useMemo, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface TrackUploadCardProps {
  label: string;
  title: string;
  artist: string;
  bpm: number;
  camelot: string;
  duration: string;
  accentColor: string;
  compact?: boolean;
  audioSrc?: string;
  active?: boolean;
}

function fmt(t: number) {
  const m = Math.floor(t / 60);
  const s = Math.floor(t % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export function TrackUploadCard({
  label,
  title,
  artist,
  bpm,
  camelot,
  duration,
  accentColor,
  compact = false,
  audioSrc,
  active = false,
}: TrackUploadCardProps) {
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [audioDuration, setAudioDuration] = useState(0);
  const [mediaError, setMediaError] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const seekRef = useRef<HTMLDivElement | null>(null);

  const togglePlay = useCallback(() => {
    if (mediaError) return;
    setPlaying((p) => !p);
  }, [mediaError]);

  const handleSeek = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    if (!audioRef.current || !seekRef.current) return;
    const rect = seekRef.current.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    audioRef.current.currentTime = x * audioDuration;
  }, [audioDuration]);

  useEffect(() => {
    if (!audioSrc) return;
    const el = new Audio(audioSrc);
    el.preload = "metadata";
    el.ontimeupdate = () => { setCurrentTime(el.currentTime); };
    el.onloadedmetadata = () => { setMediaError(false); setAudioDuration(el.duration); };
    el.onended = () => setPlaying(false);
    el.onpause = () => setPlaying(false);
    el.onerror = () => { setPlaying(false); setMediaError(true); };
    audioRef.current = el;
    return () => {
      el.pause();
      el.src = "";
    };
  }, [audioSrc]);

  useEffect(() => {
    if (!audioRef.current) return;
    if (playing) {
      void audioRef.current.play().catch(() => {
        setPlaying(false);
        setMediaError(true);
      });
    } else {
      audioRef.current.pause();
    }
  }, [playing]);

  const waveformBars = useMemo(
    () => Array.from({ length: compact ? 30 : 40 }, (_, i) => ((i * 19 + 7) % 22) + 6),
    [compact]
  );

  const progress = audioDuration > 0 ? currentTime / audioDuration : 0;
  const highlighted = playing || active;

  return (
    <motion.div
      layout
      animate={{
        borderColor: highlighted ? `${accentColor}80` : "rgba(63, 63, 70, 0.6)",
        boxShadow: highlighted
          ? `0 0 0 1px ${accentColor}18, 0 18px 55px -22px ${accentColor}75, inset 0 1px 0 ${accentColor}22`
          : "0 0 0 0 transparent",
        x: highlighted ? [0, -0.5, 0.6, -0.3, 0.4, 0] : 0,
        y: highlighted ? [0, -0.4, 0.3, -0.2, 0.35, 0] : 0,
        scale: highlighted ? [1, 1.002, 1, 1.0025, 1] : 1,
      }}
      transition={{
        borderColor: { duration: 0.35, ease: "easeOut" },
        boxShadow: { duration: 0.35, ease: "easeOut" },
        x: { duration: 0.9, repeat: highlighted ? Infinity : 0, ease: "easeInOut" },
        y: { duration: 1.05, repeat: highlighted ? Infinity : 0, ease: "easeInOut" },
        scale: { duration: 1.4, repeat: highlighted ? Infinity : 0, ease: "easeInOut" },
      }}
      className="group relative overflow-hidden rounded-2xl border bg-card/50 p-5 backdrop-blur-sm transition-colors duration-500 hover:border-border-light"
    >
      <motion.div
        initial={false}
        animate={{
          rotate: highlighted ? 360 : 0,
          opacity: highlighted ? 1 : 0,
        }}
        transition={{
          rotate: { duration: 2.2, repeat: highlighted ? Infinity : 0, ease: "linear" },
          opacity: { duration: 0.3 },
        }}
        className="pointer-events-none absolute -inset-[65%]"
        style={{
          background: `conic-gradient(from 0deg, transparent 0deg, transparent 245deg, ${accentColor}20 285deg, ${accentColor} 320deg, transparent 350deg)`,
        }}
      />
      <div className="pointer-events-none absolute inset-px rounded-[15px] bg-card" />
      <motion.div
        animate={{ opacity: highlighted ? 1 : 0 }}
        transition={{ duration: 0.35 }}
        className="pointer-events-none absolute inset-0"
        style={{
          background: `linear-gradient(145deg, ${accentColor}18, transparent 58%)`,
        }}
      />
      <motion.div
        animate={{ scaleX: highlighted ? 1 : 0, opacity: highlighted ? 1 : 0 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
        className="absolute inset-x-0 top-0 h-0.5 origin-left"
        style={{
          background: `linear-gradient(90deg, transparent, ${accentColor}, transparent)`,
          boxShadow: `0 0 18px ${accentColor}`,
        }}
      />
      <div className="pointer-events-none absolute -inset-1 opacity-0 transition-opacity duration-500 group-hover:opacity-20 blur-xl"
        style={{ background: `radial-gradient(ellipse at center, ${accentColor}, transparent)` }}
      />
      <div className="relative">
        <div className="mb-3 flex items-center justify-between">
          <span className="text-[10px] font-semibold uppercase tracking-[0.2em]" style={{ color: accentColor }}>
            {label}
          </span>
          <div className="flex items-center gap-2">
            {highlighted ? (
              <motion.span
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[8px] font-bold uppercase tracking-wider"
                style={{ color: accentColor, backgroundColor: `${accentColor}18` }}
              >
                <span className="h-1.5 w-1.5 animate-pulse rounded-full" style={{ backgroundColor: accentColor }} />
                Now playing
              </motion.span>
            ) : null}
            <span className="text-[10px] text-text-tertiary">{duration}</span>
          </div>
        </div>
        <h3 className="font-semibold text-text leading-snug text-sm">{title}</h3>
        <p className="mt-0.5 text-xs text-text-tertiary">{artist}</p>

        <div className="mt-3 flex items-center gap-3">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={togglePlay}
            disabled={mediaError || !audioSrc}
            aria-label={mediaError ? `${label} preview unavailable` : `Play ${label} preview`}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full transition-colors"
            style={{ backgroundColor: `${accentColor}20`, color: accentColor }}
          >
            {mediaError ? (
              <span className="text-xs font-bold">!</span>
            ) : playing ? (
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                <rect x="6" y="4" width="4" height="16" rx="1" />
                <rect x="14" y="4" width="4" height="16" rx="1" />
              </svg>
            ) : (
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5,3 19,12 5,21" />
              </svg>
            )}
          </motion.button>

          <div className="flex flex-1 items-end gap-[1.5px]" style={{ height: compact ? 24 : 32 }}>
            <AnimatePresence mode="popLayout">
              {waveformBars.map((h, i) => {
                const pos = i / waveformBars.length;
                const isPlayed = pos <= progress;
                const animatedH = playing
                  ? Math.min(h + ((i * 11 + 5) % 14), compact ? 24 : 32)
                  : h * 0.35;
                return (
                  <motion.div
                    key={`${i}-${playing}`}
                    animate={{ height: animatedH }}
                    transition={{ duration: playing ? 0.06 : 0.3, ease: "easeOut" }}
                    className="flex-1 rounded-full"
                    style={{
                      background: `linear-gradient(to top, ${accentColor}${isPlayed ? "88" : "22"}, ${accentColor}${isPlayed ? "CC" : "44"})`,
                      minHeight: 2,
                    }}
                  />
                );
              })}
            </AnimatePresence>
          </div>
        </div>

        <div
          ref={seekRef}
          onClick={handleSeek}
          className="group/seeker relative mt-2 h-1.5 cursor-pointer overflow-hidden rounded-full bg-zinc-800"
        >
          <motion.div
            animate={{ width: `${progress * 100}%` }}
            transition={{ duration: 0.1, ease: "linear" }}
            className="absolute inset-y-0 left-0 rounded-full"
            style={{ background: `linear-gradient(90deg, ${accentColor}, ${accentColor}cc)` }}
          />
        </div>

        <div className="mt-1 flex items-center justify-between text-[9px] text-text-tertiary">
          <span>{fmt(currentTime)}</span>
          <span>{fmt(audioDuration)}</span>
        </div>

        <div className="mt-3 flex items-center gap-4 border-t border-border/30 pt-3">
          <div className="flex items-center gap-1.5">
            <span className="text-[9px] font-medium text-text-tertiary">BPM</span>
            <span className="text-xs font-semibold text-text">{bpm}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-[9px] font-medium text-text-tertiary">Camelot</span>
            <span className="text-xs font-semibold text-text">{camelot}</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
