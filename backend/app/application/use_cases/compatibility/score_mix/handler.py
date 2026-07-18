from __future__ import annotations

from app.application.use_cases.compatibility.score_mix.command import ScoreMixCommand
from app.application.use_cases.compatibility.score_mix.dto import ScoreMixOutput
from app.application.use_cases.compatibility.score_mix.service import (
    MixScoringService,
    mix_scoring_service,
)


class ScoreMixHandler:
    def __init__(self, service: MixScoringService | None = None) -> None:
        self._service = service or mix_scoring_service

    def handle(self, command: ScoreMixCommand) -> ScoreMixOutput:
        result = self._service.compute(
            compatibility_score=command.compatibility_score,
            tempo_difference=command.tempo_difference,
            energy_difference=command.energy_difference,
        )
        return ScoreMixOutput(
            dj_score=result.dj_score,
            mix_difficulty=result.mix_difficulty,
            recommended_transition_length=result.recommended_transition_length,
        )


score_mix_handler = ScoreMixHandler()
