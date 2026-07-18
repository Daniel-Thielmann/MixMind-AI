from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StoredMedia(BaseModel):
    filename: str
    object_path: str
    content_type: str
    size_bytes: int = Field(gt=0)
    checksum_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    url: str | None = None


class SignedMediaUrl(BaseModel):
    object_path: str
    url: str
    expires_at: int


class DemoMediaAsset(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    object_path: str = Field(alias="objectPath")
    mime_type: str = Field(alias="mimeType")
    size_bytes: int = Field(alias="sizeBytes", gt=0)
    checksum: str
    duration: float | None = Field(default=None, gt=0)
    source_start: float | None = Field(default=None, alias="sourceStart", ge=0)
    source_end: float | None = Field(default=None, alias="sourceEnd", ge=0)
    url: str | None = None


class DemoMediaManifest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    source: str
    processed_at: str = Field(alias="processedAt")
    pipeline_version: str = Field(alias="pipelineVersion")
    attribution: str
    assets: dict[str, DemoMediaAsset]
    expires_at: int | None = Field(default=None, alias="expiresAt")
