export type VideoState =
  | "idle"
  | "loading"
  | "ready"
  | "playing"
  | "paused"
  | "ended"
  | "error";

export interface TrackInfo {
  name: string;
  artist: string;
  color: string;
  bpm: number;
  key: string;
  camelot: string;
}

export interface Chapter {
  time: number;
  label: string;
  type?: "track-a" | "track-b" | "blend" | "peak" | "transition";
}

export interface TransitionZone {
  startTime: number;
  endTime: number;
  label: string;
  type: "blend" | "eq-swap" | "bass-transfer" | "phrase-match";
}

export interface AIInsight {
  time: number;
  duration: number;
  type: "transition" | "eq-swap" | "bass-transfer" | "phrase-match" | "camelot-match" | "energy-shift" | "confidence";
  title: string;
  description: string;
  confidence?: number;
}

export interface Marker {
  time: number;
  label: string;
  type: "start" | "blend" | "peak" | "end" | "chapter" | "event";
  reached?: boolean;
}

export interface DemoMetadata {
  src: string;
  poster: string;
  thumbnail: string;
  title: string;
  duration: number;
  tracks: {
    a: TrackInfo;
    b: TrackInfo;
  };
  chapters: Chapter[];
  insights: AIInsight[];
  markers: Marker[];
  transitionZones: TransitionZone[];
  compatibility: {
    score: number;
    harmonicMatch: boolean;
    camelotTransition: string;
    bpmDiff: number;
    energyDiff: number;
  };
}

export interface PlayerAPI {
  play: () => void;
  pause: () => void;
  toggle: () => void;
  seek: (time: number) => void;
  setVolume: (volume: number) => void;
  toggleMute: () => void;
  toggleFullscreen: () => void;
  togglePiP: () => void;
  setPlaybackRate: (rate: number) => void;
  getCurrentTime: () => number;
  getDuration: () => number;
}

export interface MixMindVideoProps {
  src: string;
  poster?: string;
  className?: string;
  metadata?: DemoMetadata;
  onPlay?: () => void;
  onPause?: () => void;
  onEnded?: () => void;
  onTimeUpdate?: (time: number) => void;
  onSeek?: (time: number) => void;
  onMarkerReached?: (marker: Marker) => void;
  onStateChange?: (state: VideoState) => void;
  playerRef?: React.Ref<PlayerAPI>;
}
