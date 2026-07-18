from __future__ import annotations

from pydantic import BaseModel

from app.domain.value_objects.compatibility import CompatibilityResult


class CompareTracksInput(BaseModel):
    camelot_a: str
    camelot_b: str
    bpm_a: float
    bpm_b: float
    energy_a: float
    energy_b: float


class CompareTracksOutput(BaseModel):
    compatibility: CompatibilityResult
