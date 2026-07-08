from fastapi import APIRouter

from app.domain.schemas import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def read_health() -> HealthResponse:
    return HealthResponse(status="ok", service="api")
