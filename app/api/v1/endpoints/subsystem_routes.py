from fastapi import APIRouter, HTTPException

from app.services.finance_service import (
    get_subsystem_cost,
    get_cost_breakdown,
    get_budget_comparison,
    get_overrun_risk,
    get_financial_summary
)

from app.models.finance_models import (
    CostResponse,
    CostBreakdownResponse,
    BudgetComparisonResponse,
    OverrunRiskResponse,
    FinancialSummaryResponse
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

@router.get(
    "/budget-comparison/{subsystem_id}",
    response_model=BudgetComparisonResponse
)
def fetch_budget_comparison(subsystem_id: int):

    result = get_budget_comparison(subsystem_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Subsystem not found"
        )

    return result

@router.get(
    "/overrun-risk/{subsystem_id}",
    response_model=OverrunRiskResponse
)
def fetch_overrun_risk(subsystem_id: int):

    result = get_overrun_risk(subsystem_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Subsystem not found"
        )

    return result

@router.get(
    "/financial-summary/{subsystem_id}",
    response_model=FinancialSummaryResponse
)
def fetch_financial_summary(subsystem_id: int):

    result = get_financial_summary(subsystem_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Subsystem not found"
        )

    return result