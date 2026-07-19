import hashlib
import hmac
import time
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.domain.repositories.track_repository import TrackRepository
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.sqlalchemy_track_repository import (
    SqlAlchemyTrackRepository,
)

DatabaseSession = Annotated[Session, Depends(get_db)]


def _validate_signed_user(
    *,
    user_id: str | None,
    timestamp: str | None,
    signature: str | None,
    scope: str | None = None,
    max_age_seconds: int = 60,
) -> str:
    if not settings.INTERNAL_AUTH_SECRET:
        return "anonymous"
    if not user_id or not timestamp or not signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    try:
        issued_at = int(timestamp)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication timestamp",
        ) from exc
    if abs(int(time.time()) - issued_at) > max_age_seconds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired authentication signature",
        )

    payload = f"{user_id}:{timestamp}"
    if scope:
        payload = f"{payload}:{scope}"
    expected = hmac.new(
        settings.INTERNAL_AUTH_SECRET.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication signature",
        )
    return user_id


def get_current_owner_id(
    user_id: Annotated[str | None, Header(alias="X-MixMind-User")] = None,
    timestamp: Annotated[str | None, Header(alias="X-MixMind-Timestamp")] = None,
    signature: Annotated[str | None, Header(alias="X-MixMind-Signature")] = None,
) -> str:
    return _validate_signed_user(
        user_id=user_id,
        timestamp=timestamp,
        signature=signature,
    )


def get_analysis_owner_id(
    user_id: Annotated[str | None, Header(alias="X-MixMind-User")] = None,
    timestamp: Annotated[str | None, Header(alias="X-MixMind-Timestamp")] = None,
    signature: Annotated[str | None, Header(alias="X-MixMind-Signature")] = None,
    scope: Annotated[str | None, Header(alias="X-MixMind-Scope")] = None,
) -> str:
    if settings.INTERNAL_AUTH_SECRET and scope != "analysis":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scope",
        )
    return _validate_signed_user(
        user_id=user_id,
        timestamp=timestamp,
        signature=signature,
        scope="analysis",
        max_age_seconds=15 * 60,
    )


OwnerId = Annotated[str, Depends(get_current_owner_id)]
AnalysisOwnerId = Annotated[str, Depends(get_analysis_owner_id)]


def get_track_repository(db: DatabaseSession, owner_id: OwnerId) -> TrackRepository:
    return SqlAlchemyTrackRepository(db, owner_id=owner_id)


TrackRepositoryDependency = Annotated[TrackRepository, Depends(get_track_repository)]
OptionalTrackRepositoryDependency = Annotated[
    TrackRepository | None, Depends(get_track_repository)
]


def get_analysis_track_repository(
    db: DatabaseSession, owner_id: AnalysisOwnerId
) -> TrackRepository | None:
    if owner_id == "anonymous":
        return None
    return SqlAlchemyTrackRepository(db, owner_id=owner_id)


AnalysisTrackRepositoryDependency = Annotated[
    TrackRepository | None, Depends(get_analysis_track_repository)
]
