from __future__ import annotations

from fastapi import APIRouter, File, UploadFile

from app.application.dto.media import StoredMedia
from app.infrastructure.storage.storage_service import storage_service

router = APIRouter()


@router.get("/health", summary="Supabase Storage health check")
def storage_health() -> dict[str, object]:
    return storage_service.storage_health()


@router.post(
    "/videos", response_model=StoredMedia, summary="Upload a video to Supabase Storage"
)
def upload_video(video: UploadFile = File(...)) -> StoredMedia:
    path, media = storage_service.save_video_with_metadata(video)
    if media.url is not None:
        path.unlink(missing_ok=True)
    return media
