from fastapi import APIRouter, HTTPException

from app.services.finance_service import (
    get_subsystem_cost,
    get_cost_breakdown
)

from app.models.finance_models import (
    CostResponse,
    CostBreakdownResponse
)

router = APIRouter()


@router.get(
    "/costs/{subsystem_id}",
    response_model=CostResponse
)
def fetch_subsystem_cost(subsystem_id: int):

    result = get_subsystem_cost(subsystem_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Subsystem not found"
        )

    return result


@router.get(
    "/breakdown/{subsystem_id}",
    response_model=CostBreakdownResponse
)
def fetch_cost_breakdown(subsystem_id: int):

    result = get_cost_breakdown(subsystem_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Subsystem not found"
        )

    return result