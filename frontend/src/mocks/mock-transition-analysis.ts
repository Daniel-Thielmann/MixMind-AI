import type { TransitionAnalysis } from "@/types/transition-analysis";

export const MOCK_TRANSITION_ANALYSIS: TransitionAnalysis = {
  id: "mix-2026-07-18-001",
  timestamp: "2026-07-18T06:30:00Z",
  videoId: "GtSCkHk9fLw",

  tracks: {
    a: {
      name: "Samba",
      artist: "VXSION & Luch-E",
      color: "#44f3d0",
      bpm: 124,
      key: "A Minor",
      camelot: "8A",
    },
    b: {
      name: "Povoada (Remix)",
      artist: "Maz (BR), Antdot & Sued Nunes",
      color: "#8b5cf6",
      bpm: 126,
      key: "C Major",
      camelot: "8B",
    },
  },

  overallScore: 9.7,
  aiConfidence: 98.4,
  transitionType: "Progressive Harmonic Blend",
  duration: 164,

  regions: [
    {
      startTime: 0,
      endTime: 18,
      label: "Track A",
      color: "#44f3d0",
      type: "track-a",
      description: "Samba by VXSION & Luch-E playing alone — establishing the groove, key, and energy level.",
    },
    {
      startTime: 18,
      endTime: 42,
      label: "Build Up",
      color: "#a78bfa",
      type: "build-up",
      description: "EQ shaping begins. Low frequencies from Track A start to roll off as anticipation builds.",
    },
    {
      startTime: 42,
      endTime: 60,
      label: "Phrase Match",
      color: "#f59e0b",
      type: "phrase-match",
      description: "AI detects 8-bar phrase alignment. Both tracks are locked at the phrase level — critical for seamless blending.",
    },
    {
      startTime: 60,
      endTime: 83,
      label: "EQ Blend",
      color: "#44f3d0",
      type: "eq-blend",
      description: "High-pass filter on Track A. Low-end from Track B begins to take over. Frequencies are interleaving cleanly.",
    },
    {
      startTime: 83,
      endTime: 105,
      label: "Bass Transfer",
      color: "#ec4899",
      type: "bass-transfer",
      description: "Bass line transitions from A Minor root to C Major progression. Energy remains constant during the swap.",
    },
    {
      startTime: 105,
      endTime: 125,
      label: "Peak Harmony",
      color: "#44f3d0",
      type: "peak-harmony",
      description: "Both tracks playing simultaneously at maximum harmonic compatibility. Camelot 8A → 8B confirmed.",
    },
    {
      startTime: 125,
      endTime: 164,
      label: "Track B Dominant",
      color: "#8b5cf6",
      type: "track-b",
      description: "Povoada (Remix) takes full control. Transition complete. Energy level sustained through the handoff.",
    },
  ],

  events: [
    {
      time: 0,
      label: "Track A Dominant",
      description: "Samba playing solo — 124 BPM, A Minor, Camelot 8A",
      type: "track-dominant",
      severity: "info",
    },
    {
      time: 18,
      label: "Build-Up Started",
      description: "EQ shaping initiated. High-pass filter engaging on Track A low end.",
      type: "build-up",
      severity: "info",
    },
    {
      time: 42,
      label: "Phrase Match Detected",
      description: "8-bar phrase alignment confirmed — both tracks locked at structural level.",
      type: "phrase-match",
      severity: "success",
    },
    {
      time: 60,
      label: "EQ Blend Initiated",
      description: "Frequency interleaving: Track A high-passed, Track B low-end introduced.",
      type: "eq-blend",
      severity: "info",
    },
    {
      time: 78,
      label: "Bass Transfer",
      description: "Bass line shifting from A Minor root to C Major — no energy loss detected.",
      type: "bass-transfer",
      severity: "warning",
    },
    {
      time: 83,
      label: "Peak Harmonic Compatibility",
      description: "Maximum Camelot overlap — both tracks fully blended with zero harmonic conflict.",
      type: "energy-peak",
      severity: "peak",
    },
    {
      time: 105,
      label: "Vocal Layer Introduced",
      description: "Povoada vocal enters over Samba's percussion — complementary frequency ranges.",
      type: "vocal-layer",
      severity: "success",
    },
    {
      time: 125,
      label: "Track B Dominant",
      description: "Track A fully removed. Povoada (Remix) at full energy.",
      type: "track-dominant",
      severity: "info",
    },
    {
      time: 145,
      label: "Mix Stabilized",
      description: "Transition complete. Energy, EQ, and spatial positioning fully settled.",
      type: "mix-stabilize",
      severity: "success",
    },
    {
      time: 164,
      label: "Transition Complete",
      description: "AI analysis finalized. Overall score: 9.7/10.",
      type: "transition-complete",
      severity: "success",
    },
  ],

  metrics: {
    camelotMatch: "8A → 8B",
    phraseAlignment: "Perfect",
    beatSync: 99.3,
    bassTransition: "Excellent",
    eqSwap: "Smooth",
    energyTransfer: 96,
    grooveContinuity: 98,
    dancefloorPrediction: "Very High",
    mixStability: "Excellent",
  },

  justification:
    "The transition presented excellent harmonic compatibility between both tracks. " +
    "The DJ initiated the bass transfer exactly at the start of a new 16-bar phrase, " +
    "preserving dancefloor energy throughout the entire mix. BPM remained nearly constant " +
    "(124 → 126 BPM, +2 BPM difference) with AI-confirmed beat sync at 99.3%. " +
    "EQ interleaving was executed with precision: Track A high-passed gradually while " +
    "Track B low-end was introduced, resulting in zero frequency masking. " +
    "Camelot transition 8A → 8B (+1) is optimal — tracks are harmonically related " +
    "on the Camelot wheel, ensuring no key clash during the overlap. " +
    "The 8-bar phrase match at 00:42 was the critical structural moment that made " +
    "this transition feel seamless. Energy curve shows a smooth 0.78 → 0.85 ramp " +
    "with no abrupt drops, confirming excellent mix stability.",
};
