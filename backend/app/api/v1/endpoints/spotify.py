from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.dependencies import DatabaseSession, get_current_owner_id
from app.application.dto.spotify import (
    SpotifyAuthorizeUrlResponse,
    SpotifyConnectionStatusResponse,
)
from app.application.use_cases.spotify.complete_connect import (
    CompleteSpotifyConnectionUseCase,
)
from app.application.use_cases.spotify.disconnect import DisconnectSpotifyUseCase
from app.application.use_cases.spotify.get_status import (
    GetSpotifyConnectionStatusUseCase,
)
from app.application.use_cases.spotify.start_connect import (
    StartSpotifyConnectUseCase,
)
from app.core.config import settings
from app.infrastructure.repositories.sqlalchemy_spotify_repository import (
    SqlAlchemySpotifyConnectionRepository,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/integrations/spotify", tags=["Integrations"])


def _get_repository(db: Session) -> SqlAlchemySpotifyConnectionRepository:
    return SqlAlchemySpotifyConnectionRepository(db)


@router.get("/status", response_model=SpotifyConnectionStatusResponse)
def get_status(
    db: DatabaseSession,
    user_id: str = Depends(get_current_owner_id),
) -> SpotifyConnectionStatusResponse:
    use_case = GetSpotifyConnectionStatusUseCase(
        repository=_get_repository(db),
    )
    return use_case.execute(user_id)


@router.get("/connect", response_model=SpotifyAuthorizeUrlResponse)
def connect(
    db: DatabaseSession,
    user_id: str = Depends(get_current_owner_id),
) -> SpotifyAuthorizeUrlResponse:
    use_case = StartSpotifyConnectUseCase(
        repository=_get_repository(db),
    )
    return use_case.execute(user_id)


@router.get("/callback")
def callback(
    db: DatabaseSession,
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
) -> RedirectResponse:
    frontend_url = settings.FRONTEND_URL or "http://127.0.0.1:3000"
    redirect_to = f"{frontend_url}/dashboard/settings/integrations"

    if not state:
        return RedirectResponse(
            url=f"{redirect_to}?spotify=error&message=missing_state",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    use_case = CompleteSpotifyConnectionUseCase(
        repository=_get_repository(db),
    )
    connection, err_msg = use_case.execute(
        code=code,
        state=state,
        error=error,
    )

    if err_msg or not connection:
        from urllib.parse import quote

        return RedirectResponse(
            url=f"{redirect_to}?spotify=error&message={quote(err_msg or 'unknown')}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return RedirectResponse(
        url=f"{redirect_to}?spotify=connected",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def disconnect(
    db: DatabaseSession,
    user_id: str = Depends(get_current_owner_id),
) -> None:
    use_case = DisconnectSpotifyUseCase(
        repository=_get_repository(db),
    )
    use_case.execute(user_id)
    logger.info("Spotify disconnected for user %s", user_id)
