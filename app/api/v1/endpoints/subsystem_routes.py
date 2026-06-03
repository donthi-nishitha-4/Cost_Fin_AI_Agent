from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session
from app.models.finance_models import (
    BudgetComparisonResponse,
    CostBreakdownResponse,
    CostResponse,
    FinancialSummaryResponse,
    OverrunRiskResponse,
)
from app.services.finance_service import (
    get_budget_comparison,
    get_cost_breakdown,
    get_financial_summary,
    get_overrun_risk,
    get_subsystem_cost,
)

router = APIRouter()


@router.get("/costs/{subsystem_id}", response_model=CostResponse)
def fetch_subsystem_cost(
    subsystem_id: int,
    db: Session = Depends(get_db_session),
):
    result = get_subsystem_cost(subsystem_id, db=db)

    if not result:
        raise HTTPException(status_code=404, detail="Subsystem not found")

    return result


@router.get("/breakdown/{subsystem_id}", response_model=CostBreakdownResponse)
def fetch_cost_breakdown(
    subsystem_id: int,
    db: Session = Depends(get_db_session),
):
    result = get_cost_breakdown(subsystem_id, db=db)

    if not result:
        raise HTTPException(status_code=404, detail="Subsystem not found")

    return result


@router.get(
    "/budget-comparison/{subsystem_id}",
    response_model=BudgetComparisonResponse,
)
def fetch_budget_comparison(
    subsystem_id: int,
    db: Session = Depends(get_db_session),
):
    result = get_budget_comparison(subsystem_id, db=db)

    if not result:
        raise HTTPException(status_code=404, detail="Subsystem not found")

    return result


@router.get("/overrun-risk/{subsystem_id}", response_model=OverrunRiskResponse)
def fetch_overrun_risk(
    subsystem_id: int,
    db: Session = Depends(get_db_session),
):
    result = get_overrun_risk(subsystem_id, db=db)

    if not result:
        raise HTTPException(status_code=404, detail="Subsystem not found")

    return result


@router.get(
    "/financial-summary/{subsystem_id}",
    response_model=FinancialSummaryResponse,
)
def fetch_financial_summary(
    subsystem_id: int,
    db: Session = Depends(get_db_session),
):
    result = get_financial_summary(subsystem_id, db=db)

    if not result:
        raise HTTPException(status_code=404, detail="Subsystem not found")

    return result
