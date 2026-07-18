from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.track import AudioAnalysis


class AnalysisRepository(ABC):
    @abstractmethod
    def save_analysis(self, analysis_id: str, analysis: AudioAnalysis) -> None: ...

    @abstractmethod
    def get_analysis(self, analysis_id: str) -> AudioAnalysis | None: ...
