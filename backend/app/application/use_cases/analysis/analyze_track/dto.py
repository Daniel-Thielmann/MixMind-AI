from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.entities.recommendation import AIRecommendationResponse
from app.domain.entities.track import AudioAnalysis
from app.domain.value_objects.compatibility import CompatibilityResult
from app.domain.value_objects.visualization import Spectrograms, Waveforms


class AnalyzeTrackInput(BaseModel):
    track_a: UploadFilePlaceholder
    track_b: UploadFilePlaceholder


class UploadFilePlaceholder(BaseModel):
    filename: str
    content_type: str = "audio/mpeg"


class AnalyzeTrackOutput(BaseModel):
    analysis_id: str = Field(description="Unique identifier for this analysis session.")
    track_a: AudioAnalysis = Field(description="Analysis results for track A.")
    track_b: AudioAnalysis = Field(description="Analysis results for track B.")
    compatibility: CompatibilityResult = Field(
        description="Heuristic compatibility result for the track pair."
    )
    ai_recommendation: AIRecommendationResponse = Field(
        description="Structured DJ assistant recommendation for the track pair."
    )
    waveforms: Waveforms = Field(description="Generated waveform images.")
    spectrograms: Spectrograms = Field(description="Generated spectrogram images.")
