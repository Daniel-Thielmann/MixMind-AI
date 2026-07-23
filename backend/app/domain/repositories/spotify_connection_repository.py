from __future__ import annotations

import abc

from app.domain.entities.spotify_connection import SpotifyConnection


class SpotifyConnectionRepository(abc.ABC):
    @abc.abstractmethod
    def find_by_user_id(self, user_id: str) -> SpotifyConnection | None: ...

    @abc.abstractmethod
    def find_by_spotify_user_id(
        self, spotify_user_id: str
    ) -> SpotifyConnection | None: ...

    @abc.abstractmethod
    def save(self, connection: SpotifyConnection) -> SpotifyConnection: ...

    @abc.abstractmethod
    def delete_by_user_id(self, user_id: str) -> None: ...

    @abc.abstractmethod
    def mark_reauthorization_required(self, user_id: str) -> None: ...

    @abc.abstractmethod
    def create_oauth_state(
        self, nonce: str, user_id: str, provider: str, expires_at: int
    ) -> None: ...

    @abc.abstractmethod
    def find_oauth_state(self, nonce: str) -> object | None: ...

    @abc.abstractmethod
    def consume_oauth_state(self, nonce: str) -> bool: ...

    @abc.abstractmethod
    def delete_expired_oauth_states(self) -> None: ...
