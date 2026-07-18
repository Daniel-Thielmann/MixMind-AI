from __future__ import annotations

from app.domain.value_objects.bpm import BPM
from app.domain.value_objects.camelot_key import CamelotKey
from app.domain.value_objects.compatibility_score import CompatibilityScore
from app.domain.value_objects.energy import Energy


class HarmonicCompatibilityService:
    def score(self, camelot_a: CamelotKey, camelot_b: CamelotKey) -> float:
        return camelot_a.harmonic_similarity(camelot_b)

    def label(self, camelot_a: CamelotKey, camelot_b: CamelotKey) -> str:
        return camelot_a.similarity_label(camelot_b)


class AudioCompatibilityService:
    def __init__(self, harmonic: HarmonicCompatibilityService | None = None) -> None:
        self._harmonic = harmonic or HarmonicCompatibilityService()

    def compare(
        self,
        bpm_a: BPM,
        bpm_b: BPM,
        energy_a: Energy,
        energy_b: Energy,
        key_a: CamelotKey,
        key_b: CamelotKey,
    ) -> CompatibilityScore:
        tempo_diff = bpm_a.difference_to(bpm_b)
        energy_diff = energy_a.difference_to(energy_b)
        harmonic_factor = self._harmonic.score(key_a, key_b)

        tempo_factor = self._tempo_factor(tempo_diff)
        energy_factor = self._energy_factor(energy_diff)

        score = (
            (harmonic_factor * 40.0) + (tempo_factor * 40.0) + (energy_factor * 20.0)
        )
        return CompatibilityScore(value=round(score, 1))

    @staticmethod
    def _tempo_factor(tempo_difference: float) -> float:
        if tempo_difference <= 2.0:
            return 1.0
        if tempo_difference <= 5.0:
            return 0.75
        return 0.35

    @staticmethod
    def _energy_factor(energy_difference: float) -> float:
        return max(0.0, 1.0 - energy_difference)


harmonic_compatibility_service = HarmonicCompatibilityService()
audio_compatibility_service = AudioCompatibilityService()
