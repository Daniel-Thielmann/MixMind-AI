from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Protocol, runtime_checkable


class UploadSource(Protocol):
    """Framework-independent view of an incoming upload."""

    filename: str | None
    content_type: str | None
    file: BinaryIO


class MediaStorage(Protocol):
    """Application contract for persistent media storage."""

    def upload_file(self, local_path: Path, object_path: str) -> str | None: ...

    def create_signed_url(self, object_path: str, ttl: int | None = None) -> str: ...

    def remove_file(self, object_path: str) -> None: ...

    def health(self) -> dict[str, object]: ...


# Backwards-compatible name for older imports.
StoragePort = MediaStorage


@runtime_checkable
class AnalysisArtifactStorage(Protocol):
    def upload_artifact(self, local_path: Path, object_path: str) -> str | None: ...

    def cleanup_local(self, *paths: Path) -> None: ...
