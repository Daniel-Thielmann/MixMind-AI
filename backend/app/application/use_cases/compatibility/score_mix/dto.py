from __future__ import annotations

from typing import NamedTuple


class ScoreMixInput(NamedTuple):
    compatibility_score: float
    tempo_difference: float
    energy_difference: float


class ScoreMixOutput(NamedTuple):
    dj_score: int
    mix_difficulty: str
    recommended_transition_length: str
