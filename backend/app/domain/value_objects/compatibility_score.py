from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompatibilityScore:
    value: float

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not 0.0 <= self.value <= 100.0:
            msg = f"Compatibility score must be between 0 and 100, got {self.value}"
            raise ValueError(msg)

    @property
    def rating(self) -> str:
        if self.value >= 90.0:
            return "Excellent"
        if self.value >= 75.0:
            return "Very Good"
        if self.value >= 55.0:
            return "Good"
        if self.value >= 40.0:
            return "Fair"
        return "Poor"

    @property
    def as_int(self) -> int:
        return round(self.value)
