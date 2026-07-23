from __future__ import annotations

import logging

from app.domain.repositories.spotify_connection_repository import (
    SpotifyConnectionRepository,
)

logger = logging.getLogger(__name__)


class DisconnectSpotifyUseCase:
    def __init__(self, repository: SpotifyConnectionRepository | None = None) -> None:
        self._repository = repository

    def set_repository(self, repository: SpotifyConnectionRepository) -> None:
        self._repository = repository

    def execute(self, user_id: str) -> None:
        if not self._repository:
            return

        self._repository.delete_by_user_id(user_id)
        logger.info(
            "Spotify disconnected for user %s (tokens removed locally)", user_id
        )
