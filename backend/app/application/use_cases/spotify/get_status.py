from __future__ import annotations

from app.application.dto.spotify import SpotifyConnectionStatusResponse
from app.domain.repositories.spotify_connection_repository import (
    SpotifyConnectionRepository,
)


class GetSpotifyConnectionStatusUseCase:
    def __init__(self, repository: SpotifyConnectionRepository | None = None) -> None:
        self._repository = repository

    def set_repository(self, repository: SpotifyConnectionRepository) -> None:
        self._repository = repository

    def execute(self, user_id: str) -> SpotifyConnectionStatusResponse:
        if not self._repository:
            return SpotifyConnectionStatusResponse(connected=False)

        connection = self._repository.find_by_user_id(user_id)
        if not connection:
            return SpotifyConnectionStatusResponse(connected=False)

        return SpotifyConnectionStatusResponse(
            connected=True,
            spotify_user_id=connection.spotify_user_id,
            display_name=connection.spotify_display_name,
            email=connection.spotify_email,
            scopes=connection.scopes_list,
            connected_at=connection.created_at,
            needs_reauthorization=connection.needs_reauthorization,
        )
