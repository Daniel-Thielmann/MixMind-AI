from __future__ import annotations

import hashlib
import mimetypes
import re
from pathlib import Path
from typing import Protocol

from app.application.dto.media import StoredMedia
from app.application.ports.storage import UploadSource
from app.core.config import settings
from app.core.exceptions import (
    FileTooLargeException,
    InvalidMediaFileException,
)
from app.domain.value_objects.file_utils import generate_unique_filename
from app.infrastructure.storage.supabase_storage import build_supabase_storage

_CHUNK_SIZE = 1024 * 1024
_SAFE_STEM = re.compile(r"[^A-Za-z0-9._ -]+")
_AUDIO_TYPES = {
    ".mp3": {"audio/mpeg", "audio/mp3", "application/octet-stream"},
    ".wav": {"audio/wav", "audio/x-wav", "application/octet-stream"},
    ".flac": {"audio/flac", "audio/x-flac", "application/octet-stream"},
}
_VIDEO_TYPES = {
    ".mp4": {"video/mp4", "application/octet-stream"},
    ".webm": {"video/webm", "application/octet-stream"},
}


class RemoteStorage(Protocol):
    @property
    def bucket(self) -> str: ...

    def health(self) -> dict[str, object]: ...

    def upload_file(self, local_path: Path, object_path: str) -> str | None: ...


def _safe_filename(raw: str) -> str:
    if Path(raw).name != raw or raw in {".", ".."}:
        raise InvalidMediaFileException(raw, "Unsafe filename")
    cleaned = _SAFE_STEM.sub("_", raw).strip(" .")
    if not cleaned or cleaned in {".", ".."}:
        raise InvalidMediaFileException(raw, "Unsafe filename")
    return cleaned


def _matches_signature(suffix: str, header: bytes) -> bool:
    if suffix == ".mp3":
        return header.startswith(b"ID3") or (
            len(header) >= 2 and header[0] == 0xFF and header[1] & 0xE0 == 0xE0
        )
    if suffix == ".wav":
        return len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WAVE"
    if suffix == ".flac":
        return header.startswith(b"fLaC")
    if suffix == ".mp4":
        return len(header) >= 12 and header[4:8] == b"ftyp"
    if suffix == ".webm":
        return header.startswith(b"\x1aE\xdf\xa3")
    return False


class StorageService:
    """Validates uploads, stages them locally, and mirrors them remotely."""

    def __init__(self, remote: RemoteStorage | None = None) -> None:
        self._remote = remote if remote is not None else build_supabase_storage()

    def _save(
        self,
        upload: UploadSource,
        *,
        allowed: dict[str, set[str]],
        destination_dir: Path,
        object_prefix: str,
    ) -> tuple[Path, StoredMedia]:
        if not upload.filename:
            raise InvalidMediaFileException("<unknown>", "Missing filename")

        original_name = _safe_filename(upload.filename)
        suffix = Path(original_name).suffix.lower()
        if suffix not in allowed:
            raise InvalidMediaFileException(original_name, "Unsupported media format")

        content_type = (
            upload.content_type
            or mimetypes.guess_type(original_name)[0]
            or "application/octet-stream"
        ).lower()
        if content_type not in allowed[suffix]:
            raise InvalidMediaFileException(
                original_name, "MIME type does not match extension"
            )

        destination_dir.mkdir(parents=True, exist_ok=True)
        filename = generate_unique_filename(original_name)
        destination = destination_dir / filename
        max_bytes = getattr(settings, "MAX_UPLOAD_SIZE", 100) * 1024 * 1024
        digest = hashlib.sha256()
        size = 0
        header = b""

        try:
            with destination.open("xb") as target:
                while chunk := upload.file.read(_CHUNK_SIZE):
                    if not header:
                        header = chunk[:16]
                    size += len(chunk)
                    if size > max_bytes:
                        raise FileTooLargeException()
                    digest.update(chunk)
                    target.write(chunk)
        except Exception:
            destination.unlink(missing_ok=True)
            raise
        finally:
            upload.file.close()

        if size == 0 or not _matches_signature(suffix, header):
            destination.unlink(missing_ok=True)
            raise InvalidMediaFileException(original_name, "Media content is invalid")

        object_path = f"{object_prefix.strip('/')}/{filename}"
        url: str | None = None
        try:
            if self._remote is not None:
                url = self._remote.upload_file(destination, object_path)
        except Exception:
            destination.unlink(missing_ok=True)
            raise

        return destination, StoredMedia(
            filename=filename,
            object_path=object_path,
            content_type=content_type,
            size_bytes=size,
            checksum_sha256=digest.hexdigest(),
            url=url,
        )

    def save_audio(self, file: UploadSource) -> Path:
        path, _ = self._save(
            file,
            allowed=_AUDIO_TYPES,
            destination_dir=settings.upload_path,
            object_prefix="uploads",
        )
        return path

    def save_audio_with_metadata(
        self, file: UploadSource, object_prefix: str = "uploads"
    ) -> tuple[Path, StoredMedia]:
        return self._save(
            file,
            allowed=_AUDIO_TYPES,
            destination_dir=settings.upload_path,
            object_prefix=object_prefix,
        )

    def storage_health(self) -> dict[str, object]:
        if self._remote is None:
            return {
                "configured": False,
                "connected": False,
                "bucket": None,
                "public": False,
            }
        return self._remote.health()

    def upload_artifact(self, local_path: Path, object_path: str) -> str | None:
        if self._remote is None:
            return None
        url = self._remote.upload_file(local_path, object_path)
        local_path.unlink(missing_ok=True)
        return url

    def cleanup_local(self, *paths: Path) -> None:
        if self._remote is None:
            return
        for path in paths:
            path.unlink(missing_ok=True)

    def save_video(self, file: UploadSource) -> tuple[Path, str | None]:
        path, media = self._save(
            file,
            allowed=_VIDEO_TYPES,
            destination_dir=settings.upload_path / "videos",
            object_prefix="videos",
        )
        return path, media.url

    def save_video_with_metadata(
        self, file: UploadSource, object_prefix: str = "videos"
    ) -> tuple[Path, StoredMedia]:
        return self._save(
            file,
            allowed=_VIDEO_TYPES,
            destination_dir=settings.upload_path / "videos",
            object_prefix=object_prefix,
        )


storage_service = StorageService()
