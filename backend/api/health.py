from fastapi import APIRouter

from models.schemas import (
    HealthResponse,
)


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
)
def health():

    return HealthResponse(
        status="ok"
    )