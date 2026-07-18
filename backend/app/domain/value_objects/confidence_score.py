from __future__ import annotations

from dataclasses import dataclass

from app.domain.exceptions.domain_exceptions import InvalidConfidenceError


@dataclass(frozen=True)
class ConfidenceScore:
    value: int

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 100:
            raise InvalidConfidenceError(self.value)

    @property
    def level(self) -> str:
        if self.value >= 90:
            return "Very High"
        if self.value >= 75:
            return "High"
        if self.value >= 50:
            return "Medium"
        if self.value >= 25:
            return "Low"
        return "Very Low"
