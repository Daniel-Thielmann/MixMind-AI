from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, Field

from app.domain.events.track_events import TrackUploaded
from app.domain.value_objects.bpm import BPM
from app.domain.value_objects.camelot_key import CamelotKey
from app.domain.value_objects.duration import Duration
from app.domain.value_objects.energy import Energy
from app.domain.value_objects.identifiers import TrackId


class AudioAnalysis(BaseModel):
    """Audio metrics extracted from a track."""

    filename: str = Field(description="Original filename of the uploaded track.")
    duration: float = Field(description="Track duration in seconds.")
    sample_rate: int = Field(description="Audio sample rate in Hertz.")
    bpm: float = Field(description="Estimated tempo in beats per minute.")
    energy: float = Field(description="Average RMS energy of the track.")
    key: str = Field(
        default="Unknown", description="Musical key detected (e.g., G# Minor)."
    )
    camelot: str = Field(
        default="Unknown",
        description="Camelot wheel value for harmonic mixing (e.g., 1A).",
    )

    def to_bpm(self) -> BPM:
        return BPM(value=self.bpm)

    def to_energy(self) -> Energy:
        return Energy(value=self.energy)

    def to_duration(self) -> Duration:
        return Duration(value=self.duration)

    def to_camelot_key(self) -> CamelotKey | None:
        if self.camelot == "Unknown":
            return None
        return CamelotKey(value=self.camelot)


@dataclass
class Track:
    track_id: TrackId = field(default_factory=TrackId)
    filename: str = ""
    duration: Duration | None = None
    bpm: BPM | None = None
    energy: Energy | None = None
    key: str = "Unknown"
    camelot: CamelotKey | None = None
    sample_rate: int = 0
    owner_id: str = "anonymous"

    def analyze(self, audio_analysis: AudioAnalysis) -> None:
        self.filename = audio_analysis.filename
        self.duration = audio_analysis.to_duration()
        self.bpm = audio_analysis.to_bpm()
        self.energy = audio_analysis.to_energy()
        self.key = audio_analysis.key
        self.camelot = audio_analysis.to_camelot_key()
        self.sample_rate = audio_analysis.sample_rate

    def to_uploaded_event(self) -> TrackUploaded:
        return TrackUploaded(track_id=str(self.track_id), filename=self.filename)
