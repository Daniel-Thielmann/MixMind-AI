from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.entities.track import AudioAnalysis
from app.domain.events.track_events import TrackAnalyzed
from app.domain.exceptions.domain_exceptions import (
    AnalysisNotFoundError,
    DuplicateAnalysisError,
)
from app.domain.value_objects.identifiers import AnalysisId
from app.domain.value_objects.visualization import Spectrograms, Waveforms


@dataclass
class Analysis:
    analysis_id: AnalysisId = field(default_factory=AnalysisId)
    track_a: AudioAnalysis | None = None
    track_b: AudioAnalysis | None = None
    waveforms: Waveforms | None = None
    spectrograms: Spectrograms | None = None
    _completed: bool = False

    def add_track_a(self, analysis: AudioAnalysis) -> None:
        self.track_a = analysis

    def add_track_b(self, analysis: AudioAnalysis) -> None:
        self.track_b = analysis

    def add_visualizations(
        self, waveforms: Waveforms, spectrograms: Spectrograms
    ) -> None:
        self.waveforms = waveforms
        self.spectrograms = spectrograms

    def complete(self) -> TrackAnalyzed:
        self._completed = True
        return TrackAnalyzed(
            analysis_id=str(self.analysis_id),
            track_a_id=self.track_a.filename if self.track_a else "",
            track_b_id=self.track_b.filename if self.track_b else "",
        )

    @property
    def is_complete(self) -> bool:
        return self._completed and self.track_a is not None and self.track_b is not None


class AnalysisCollection:
    def __init__(self) -> None:
        self._analyses: dict[str, Analysis] = {}

    def add(self, analysis: Analysis) -> None:
        key = str(analysis.analysis_id)
        if key in self._analyses:
            raise DuplicateAnalysisError(key)
        self._analyses[key] = analysis

    def get(self, analysis_id: str) -> Analysis:
        if analysis_id not in self._analyses:
            raise AnalysisNotFoundError(analysis_id)
        return self._analyses[analysis_id]
