from app.core.database import SessionLocal
from app.data.evaluation_dataset_100 import SUBSYSTEM_DATA
from app.models.finance_db_models import FinanceSubsystem


def seed_finance_database(db=None):
    close_db = False

    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        existing_count = db.query(FinanceSubsystem).count()
        if existing_count > 0:
            db.query(FinanceSubsystem).delete()
            db.commit()

        for subsystem_id, data in SUBSYSTEM_DATA.items():
            row = FinanceSubsystem(
                id=subsystem_id,
                subsystem_name=data.get("subsystem_name", data.get("subsystem")),
                planned_cost=data["planned_cost"],
                actual_cost=data["actual_cost"],
                labor_cost=data["labor_cost"],
                material_cost=data["material_cost"],
                equipment_cost=data["equipment_cost"]
            )
            db.add(row)

        db.commit()
    finally:
        if close_db:
            db.close()