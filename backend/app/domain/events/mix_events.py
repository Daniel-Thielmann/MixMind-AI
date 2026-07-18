from __future__ import annotations

from dataclasses import dataclass

from app.domain.events.base import DomainEvent


@dataclass(frozen=True, kw_only=True)
class MixComputed(DomainEvent):
    mix_id: str
    analysis_id: str
    compatibility_score: float


@dataclass(frozen=True, kw_only=True)
class RecommendationGenerated(DomainEvent):
    mix_id: str
    analysis_id: str
    confidence: int
