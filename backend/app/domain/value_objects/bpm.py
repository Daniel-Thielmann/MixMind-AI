from __future__ import annotations

from dataclasses import dataclass

from app.domain.exceptions.domain_exceptions import InvalidBPMError


@dataclass(frozen=True)
class BPM:
    value: float

    def __post_init__(self) -> None:
        if not 20.0 <= self.value <= 300.0:
            raise InvalidBPMError(self.value)

    def difference_to(self, other: BPM) -> float:
        return abs(self.value - other.value)

    def is_compatible(self, other: BPM, threshold: float = 5.0) -> bool:
        return self.difference_to(other) <= threshold
