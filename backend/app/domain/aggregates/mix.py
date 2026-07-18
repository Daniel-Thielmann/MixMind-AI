from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.aggregates.analysis import Analysis
from app.domain.events.mix_events import MixComputed
from app.domain.value_objects.compatibility_score import CompatibilityScore
from app.domain.value_objects.identifiers import MixId


@dataclass
class Mix:
    mix_id: MixId = field(default_factory=MixId)
    analysis: Analysis | None = None
    compatibility_score: CompatibilityScore | None = None
    _scored: bool = False

    def score(self, score: CompatibilityScore) -> MixComputed:
        self.compatibility_score = score
        self._scored = True
        return MixComputed(
            mix_id=str(self.mix_id),
            analysis_id=str(self.analysis.analysis_id) if self.analysis else "",
            compatibility_score=score.value,
        )

    @property
    def is_scored(self) -> bool:
        return self._scored and self.compatibility_score is not None
