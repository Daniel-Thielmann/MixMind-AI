from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScoreMixCommand:
    compatibility_score: float
    tempo_difference: float
    energy_difference: float
