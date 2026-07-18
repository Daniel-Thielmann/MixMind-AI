from __future__ import annotations

from dataclasses import dataclass

from app.domain.exceptions.domain_exceptions import InvalidEnergyError


@dataclass(frozen=True)
class Energy:
    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 1.0:
            raise InvalidEnergyError(self.value)

    def difference_to(self, other: Energy) -> float:
        return round(abs(self.value - other.value), 6)

    def is_compatible(self, other: Energy, threshold: float = 0.1) -> bool:
        return self.difference_to(other) <= threshold
