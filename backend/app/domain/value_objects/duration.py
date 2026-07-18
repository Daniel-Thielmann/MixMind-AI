from __future__ import annotations

from dataclasses import dataclass

from app.domain.exceptions.domain_exceptions import InvalidDurationError


@dataclass(frozen=True)
class Duration:
    value: float

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise InvalidDurationError(self.value)

    @property
    def minutes_seconds(self) -> tuple[int, int]:
        total_seconds = int(self.value)
        return total_seconds // 60, total_seconds % 60

    def __str__(self) -> str:
        m, s = self.minutes_seconds
        return f"{m}:{s:02d}"
