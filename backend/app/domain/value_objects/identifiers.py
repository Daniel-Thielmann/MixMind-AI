from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class TrackId:
    value: str = field(default_factory=lambda: uuid4().hex)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class AnalysisId:
    value: str = field(default_factory=lambda: uuid4().hex)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class MixId:
    value: str = field(default_factory=lambda: uuid4().hex)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class PlaylistId:
    value: str = field(default_factory=lambda: uuid4().hex)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class RecommendationId:
    value: str = field(default_factory=lambda: uuid4().hex)

    def __str__(self) -> str:
        return self.value
