from __future__ import annotations

from fastapi import APIRouter

from app.application.dto.media import DemoMediaManifest
from app.infrastructure.storage.demo_media import demo_media_service

router = APIRouter()


@router.get("/manifest", response_model=DemoMediaManifest)
def get_demo_manifest() -> DemoMediaManifest:
    return demo_media_service.get_signed_manifest()
