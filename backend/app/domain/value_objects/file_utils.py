from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from app.domain.value_objects.genre import Genre

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".flac",
}


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def is_allowed_audio(filename: str) -> bool:
    return get_extension(filename) in ALLOWED_EXTENSIONS


def generate_unique_filename(filename: str) -> str:
    extension = get_extension(filename)
    stem = Path(filename).stem
    return f"{uuid4().hex}_{stem}{extension}"


def guess_genre_from_bpm(bpm: float) -> Genre:
    if bpm < 80:
        return Genre("Downbeat")
    if bpm < 110:
        return Genre("Hip-Hop")
    if bpm < 125:
        return Genre("House")
    if bpm < 140:
        return Genre("Techno")
    if bpm < 160:
        return Genre("Drum & Bass")
    return Genre("Hardcore")
