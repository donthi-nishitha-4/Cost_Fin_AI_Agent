from sqlalchemy.orm import Session

from app.models.finance_db_models import FinanceSubsystem


def get_finance_subsystem_by_id(db: Session, subsystem_id: int):
    return db.query(FinanceSubsystem).filter(FinanceSubsystem.id == subsystem_id).first()