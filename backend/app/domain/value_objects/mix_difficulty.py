from __future__ import annotations

from enum import Enum


class MixDifficulty(Enum):
    VERY_EASY = "Very Easy"
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXPERT = "Expert"

    @property
    def suggested_transition_bars(self) -> int:
        mapping = {
            MixDifficulty.VERY_EASY: 64,
            MixDifficulty.EASY: 32,
            MixDifficulty.MEDIUM: 32,
            MixDifficulty.HARD: 16,
            MixDifficulty.EXPERT: 8,
        }
        return mapping[self]
