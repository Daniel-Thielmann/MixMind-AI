from __future__ import annotations

from dataclasses import dataclass

from fastapi import UploadFile


@dataclass
class AnalyzeTrackCommand:
    track_a: UploadFile
    track_b: UploadFile
