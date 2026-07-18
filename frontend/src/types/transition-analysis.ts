export interface TrackInfo {
  name: string;
  artist: string;
  color: string;
  bpm: number;
  key: string;
  camelot: string;
}

export interface TransitionEvent {
  time: number;
  label: string;
  description: string;
  type: "phrase-match" | "eq-blend" | "bass-transfer" | "energy-peak" | "vocal-layer" | "track-dominant" | "transition-complete" | "build-up" | "mix-stabilize";
  severity: "info" | "warning" | "success" | "peak";
}

export interface TransitionRegion {
  startTime: number;
  endTime: number;
  label: string;
  color: string;
  type: "track-a" | "build-up" | "phrase-match" | "eq-blend" | "bass-transfer" | "peak-harmony" | "track-b";
  description: string;
}

export interface MetricItem {
  label: string;
  value: string | number;
  status: "excellent" | "good" | "fair";
  unit?: string;
}

export interface TransitionAnalysis {
  id: string;
  timestamp: string;
  videoId: string;
  tracks: {
    a: TrackInfo;
    b: TrackInfo;
  };
  overallScore: number;
  aiConfidence: number;
  transitionType: string;
  duration: number;
  regions: TransitionRegion[];
  events: TransitionEvent[];
  metrics: {
    camelotMatch: string;
    phraseAlignment: "Perfect" | "Good" | "Fair";
    beatSync: number;
    bassTransition: "Excellent" | "Good" | "Fair";
    eqSwap: "Smooth" | "Adequate" | "Abrupt";
    energyTransfer: number;
    grooveContinuity: number;
    dancefloorPrediction: "Very High" | "High" | "Moderate";
    mixStability: "Excellent" | "Good" | "Fair";
  };
  justification: string;
}
