from __future__ import annotations

from app.domain.entities.spotify_connection import SpotifyConnection
from app.infrastructure.database.models.spotify_connection_model import (
    SpotifyConnectionModel,
)


class SpotifyConnectionMapper:
    @staticmethod
    def to_persistence(entity: SpotifyConnection) -> SpotifyConnectionModel:
        return SpotifyConnectionModel(
            user_id=entity.user_id,
            spotify_user_id=entity.spotify_user_id,
            spotify_display_name=entity.spotify_display_name,
            spotify_email=entity.spotify_email,
            access_token=entity.access_token,
            refresh_token=entity.refresh_token,
            token_type=entity.token_type,
            scope=entity.scope,
            expires_at=entity.expires_at,
            status=entity.status,
            authorized_at=entity.authorized_at,
            last_refresh_at=entity.last_refresh_at,
        )

    @staticmethod
    def to_domain(model: SpotifyConnectionModel) -> SpotifyConnection:
        return SpotifyConnection(
            id=str(model.id),
            user_id=model.user_id,
            spotify_user_id=model.spotify_user_id,
            spotify_display_name=model.spotify_display_name,
            spotify_email=model.spotify_email,
            access_token=model.access_token,
            refresh_token=model.refresh_token,
            token_type=model.token_type,
            scope=model.scope,
            expires_at=model.expires_at,
            status=model.status,
            authorized_at=model.authorized_at,
            last_refresh_at=model.last_refresh_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
