from io import BytesIO
from types import SimpleNamespace

import pytest
from fastapi import UploadFile
from starlette.datastructures import Headers

from app.core.exceptions import FileTooLargeException, InvalidMediaFileException
from app.infrastructure.storage.storage_service import StorageService


class FakeRemoteStorage:
    bucket = "test-bucket"

    def __init__(self) -> None:
        self.uploaded: list[tuple[bytes, str]] = []

    def health(self) -> dict[str, object]:
        return {"configured": True, "connected": True, "bucket": self.bucket}

    def upload_file(self, local_path, object_path: str) -> str | None:
        self.uploaded.append((local_path.read_bytes(), object_path))
        return None


def test_save_audio_stores_bytes_in_upload_path(tmp_path, monkeypatch) -> None:
    from app.infrastructure.storage import storage_service as storage_module

    monkeypatch.setattr(
        storage_module,
        "settings",
        SimpleNamespace(upload_path=tmp_path),
    )

    service = StorageService()
    uploaded_file = UploadFile(filename="track.mp3", file=BytesIO(b"ID3abc123"))

    stored_path = service.save_audio(uploaded_file)

    assert stored_path.exists()
    assert stored_path.suffix == ".mp3"
    assert stored_path.read_bytes() == b"ID3abc123"


def test_save_audio_mirrors_file_to_remote_storage(tmp_path, monkeypatch) -> None:
    from app.infrastructure.storage import storage_service as storage_module

    monkeypatch.setattr(
        storage_module,
        "settings",
        SimpleNamespace(upload_path=tmp_path),
    )
    remote = FakeRemoteStorage()
    service = StorageService(remote=remote)
    uploaded_file = UploadFile(filename="track.mp3", file=BytesIO(b"ID3abc123"))

    stored_path = service.save_audio(uploaded_file)

    assert stored_path.exists()
    assert remote.uploaded == [(b"ID3abc123", f"uploads/{stored_path.name}")]


def test_save_video_mirrors_file_to_remote_storage(tmp_path, monkeypatch) -> None:
    from app.infrastructure.storage import storage_service as storage_module

    monkeypatch.setattr(
        storage_module,
        "settings",
        SimpleNamespace(upload_path=tmp_path),
    )
    remote = FakeRemoteStorage()
    service = StorageService(remote=remote)
    uploaded_file = UploadFile(
        filename="demo.mp4", file=BytesIO(b"\x00\x00\x00\x18ftypmp42video")
    )

    stored_path, url = service.save_video(uploaded_file)

    assert stored_path.exists()
    assert url is None
    assert remote.uploaded == [
        (b"\x00\x00\x00\x18ftypmp42video", f"videos/{stored_path.name}")
    ]


@pytest.mark.parametrize(
    ("filename", "content", "content_type"),
    [
        ("empty.mp3", b"", "audio/mpeg"),
        ("fake.mp3", b"not-an-mp3", "audio/mpeg"),
        ("track.mp3", b"ID3valid", "video/mp4"),
        ("../track.mp3", b"ID3valid", "audio/mpeg"),
    ],
)
def test_invalid_uploads_are_rejected_and_cleaned(
    tmp_path, monkeypatch, filename, content, content_type
) -> None:
    from app.infrastructure.storage import storage_service as storage_module

    monkeypatch.setattr(
        storage_module,
        "settings",
        SimpleNamespace(upload_path=tmp_path, MAX_UPLOAD_SIZE=100),
    )
    upload = UploadFile(
        filename=filename,
        file=BytesIO(content),
        headers=Headers({"content-type": content_type}),
    )
    with pytest.raises(InvalidMediaFileException):
        StorageService(remote=FakeRemoteStorage()).save_audio(upload)
    assert list(tmp_path.glob("*")) == []


def test_upload_size_limit_is_enforced_and_partial_file_removed(
    tmp_path, monkeypatch
) -> None:
    from app.infrastructure.storage import storage_service as storage_module

    monkeypatch.setattr(
        storage_module,
        "settings",
        SimpleNamespace(upload_path=tmp_path, MAX_UPLOAD_SIZE=0),
    )
    upload = UploadFile(filename="track.mp3", file=BytesIO(b"ID3content"))
    with pytest.raises(FileTooLargeException):
        StorageService(remote=FakeRemoteStorage()).save_audio(upload)
    assert list(tmp_path.glob("*")) == []


def test_upload_metadata_contains_sha256(tmp_path, monkeypatch) -> None:
    from app.infrastructure.storage import storage_service as storage_module

    monkeypatch.setattr(
        storage_module,
        "settings",
        SimpleNamespace(upload_path=tmp_path, MAX_UPLOAD_SIZE=100),
    )
    _, media = StorageService(remote=FakeRemoteStorage()).save_audio_with_metadata(
        UploadFile(filename="track.mp3", file=BytesIO(b"ID3content"))
    )
    assert len(media.checksum_sha256) == 64
    assert media.size_bytes == len(b"ID3content")
