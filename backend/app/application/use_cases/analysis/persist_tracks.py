from __future__ import annotations

from app.domain.entities.track import AudioAnalysis, Track
from app.domain.repositories.track_repository import TrackRepository


class PersistAnalyzedTracks:
    def __init__(self, repository: TrackRepository) -> None:
        self._repository = repository

    def execute(self, *analyses: AudioAnalysis) -> None:
        for analysis in analyses:
            track = Track()
            track.analyze(analysis)
            self._repository.save(track)
