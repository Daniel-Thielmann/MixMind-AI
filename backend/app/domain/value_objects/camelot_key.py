from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.domain.exceptions.domain_exceptions import InvalidCamelotKeyError


class CamelotLetter(Enum):
    A = "A"
    B = "B"


_INNER_WHEEL = {
    "1A",
    "2A",
    "3A",
    "4A",
    "5A",
    "6A",
    "7A",
    "8A",
    "9A",
    "10A",
    "11A",
    "12A",
}
_OUTER_WHEEL = {
    "1B",
    "2B",
    "3B",
    "4B",
    "5B",
    "6B",
    "7B",
    "8B",
    "9B",
    "10B",
    "11B",
    "12B",
}
_ALL_KEYS = _INNER_WHEEL | _OUTER_WHEEL


@dataclass(frozen=True)
class CamelotKey:
    value: str

    def __post_init__(self) -> None:
        if self.value not in _ALL_KEYS:
            raise InvalidCamelotKeyError(self.value)

    @property
    def number(self) -> int:
        return int(self.value[:-1])

    @property
    def letter(self) -> CamelotLetter:
        return CamelotLetter(self.value[-1])

    def is_perfect_match(self, other: CamelotKey) -> bool:
        return self.value == other.value

    def is_relative_match(self, other: CamelotKey) -> bool:
        return self.number == other.number and self.letter != other.letter

    def is_adjacent_match(self, other: CamelotKey) -> bool:
        if self.letter != other.letter:
            return False
        diff = abs(self.number - other.number)
        return diff == 1 or diff == 11

    def is_energy_boost(self, other: CamelotKey) -> bool:
        if self.letter != other.letter:
            return False
        diff = abs(self.number - other.number)
        return diff == 2 or diff == 10

    def harmonic_similarity(self, other: CamelotKey) -> float:
        if self.is_perfect_match(other):
            return 1.0
        if self.is_relative_match(other) or self.is_adjacent_match(other):
            return 0.8
        if self.is_energy_boost(other):
            return 0.6
        return 0.0

    def similarity_label(self, other: CamelotKey) -> str:
        sim = self.harmonic_similarity(other)
        if sim == 1.0:
            return "Perfect"
        if sim == 0.8:
            rel = "Relative" if self.is_relative_match(other) else "Adjacent"
            return f"Good ({rel})"
        if sim == 0.6:
            return "Fair (Energy Boost)"
        return "Clash"

    def to_musical_key(self) -> str:
        mapping = {
            "1A": "C Minor",
            "2A": "G Minor",
            "3A": "D Minor",
            "4A": "A Minor",
            "5A": "E Minor",
            "6A": "B Minor",
            "7A": "F# Minor",
            "8A": "C# Minor",
            "9A": "G# Minor",
            "10A": "D# Minor",
            "11A": "A# Minor",
            "12A": "F Minor",
            "1B": "C Major",
            "2B": "G Major",
            "3B": "D Major",
            "4B": "A Major",
            "5B": "E Major",
            "6B": "B Major",
            "7B": "F# Major",
            "8B": "C# Major",
            "9B": "G# Major",
            "10B": "D# Major",
            "11B": "A# Major",
            "12B": "F Major",
        }
        return mapping.get(self.value, "Unknown")
