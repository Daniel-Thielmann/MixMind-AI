from __future__ import annotations

from dataclasses import dataclass

from app.application.ports.storage import UploadSource


@dataclass
class AnalyzeTrackCommand:
    track_a: UploadSource
    track_b: UploadSource
