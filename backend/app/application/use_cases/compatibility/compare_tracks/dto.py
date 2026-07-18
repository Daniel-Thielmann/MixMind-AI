from __future__ import annotations

from app.domain.value_objects.compatibility import CompatibilityResult
from pydantic import BaseModel


class CompareTracksInput(BaseModel):
    camelot_a: str
    camelot_b: str
    bpm_a: float
    bpm_b: float
    energy_a: float
    energy_b: float


class CompareTracksOutput(BaseModel):
    compatibility: CompatibilityResult
