from __future__ import annotations

from app.application.use_cases.analysis.analyze_track.command import (
    AnalyzeTrackCommand,
)
from app.application.use_cases.analysis.analyze_track.dto import AnalyzeTrackOutput
from app.application.use_cases.analysis.analyze_track.service import (
    AnalysisService,
    analysis_service,
)


class AnalyzeTrackHandler:
    def __init__(self, service: AnalysisService | None = None) -> None:
        self._service = service or analysis_service

    def handle(self, command: AnalyzeTrackCommand) -> AnalyzeTrackOutput:
        response = self._service.analyze(command.track_a, command.track_b)
        return AnalyzeTrackOutput(
            analysis_id=response.analysis_id,
            track_a=response.track_a,
            track_b=response.track_b,
            compatibility=response.compatibility,
            ai_recommendation=response.ai_recommendation,
            waveforms=response.waveforms,
            spectrograms=response.spectrograms,
        )


analyze_track_handler = AnalyzeTrackHandler()
