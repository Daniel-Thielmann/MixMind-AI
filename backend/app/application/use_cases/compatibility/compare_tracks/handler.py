from __future__ import annotations

from app.application.use_cases.compatibility.compare_tracks.command import (
    CompareTracksCommand,
)
from app.application.use_cases.compatibility.compare_tracks.dto import (
    CompareTracksOutput,
)
from app.application.use_cases.compatibility.compare_tracks.service import (
    CompatibilityService,
    compatibility_service,
)


class CompareTracksHandler:
    def __init__(self, service: CompatibilityService | None = None) -> None:
        self._service = service or compatibility_service

    def handle(self, command: CompareTracksCommand) -> CompareTracksOutput:
        result = self._service.compare(command.track_a, command.track_b)
        return CompareTracksOutput(compatibility=result)


compare_tracks_handler = CompareTracksHandler()
