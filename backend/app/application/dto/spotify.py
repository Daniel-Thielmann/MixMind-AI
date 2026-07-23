from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class SpotifyConnectionStatusResponse(BaseModel):
    connected: bool
    spotify_user_id: str | None = None
    display_name: str | None = None
    email: str | None = None
    scopes: list[str] = []
    connected_at: datetime | None = None
    needs_reauthorization: bool = False


class SpotifyAuthorizeUrlResponse(BaseModel):
    authorization_url: str


class SpotifyErrorResponse(BaseModel):
    detail: str
