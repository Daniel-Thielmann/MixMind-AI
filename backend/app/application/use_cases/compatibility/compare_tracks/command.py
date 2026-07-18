from __future__ import annotations

from dataclasses import dataclass

from app.domain.entities.track import AudioAnalysis


@dataclass
class CompareTracksCommand:
    track_a: AudioAnalysis
    track_b: AudioAnalysis
