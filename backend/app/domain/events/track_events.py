from __future__ import annotations

from dataclasses import dataclass

from app.domain.events.base import DomainEvent


@dataclass(frozen=True, kw_only=True)
class TrackUploaded(DomainEvent):
    track_id: str
    filename: str


@dataclass(frozen=True, kw_only=True)
class TrackAnalyzed(DomainEvent):
    analysis_id: str
    track_a_id: str
    track_b_id: str
