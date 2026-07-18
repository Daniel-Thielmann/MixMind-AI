from fastapi import APIRouter, File, UploadFile

from app.api.dependencies import OptionalTrackRepositoryDependency, OwnerId
from app.application.dto.api import UploadAnalysisResponse
from app.application.use_cases.analysis.analyze_track import analysis_service
from app.application.use_cases.analysis.persist_tracks import PersistAnalyzedTracks

router = APIRouter()


@router.get("/")
async def analysis_status() -> dict[str, str]:
    return {
        "service": "Analysis Service",
        "status": "available",
    }


@router.post(
    "/analyze",
    response_model=UploadAnalysisResponse,
    summary="Upload and analyze two tracks",
)
async def analyze_tracks(
    track_a: UploadFile = File(...),
    track_b: UploadFile = File(...),
    repository: OptionalTrackRepositoryDependency = None,
    owner_id: OwnerId = "anonymous",
) -> UploadAnalysisResponse:
    response = analysis_service.analyze(track_a, track_b)
    if repository is not None and owner_id != "anonymous":
        PersistAnalyzedTracks(repository).execute(response.track_a, response.track_b)
    return response
