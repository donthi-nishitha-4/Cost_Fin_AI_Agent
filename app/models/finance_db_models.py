from sqlalchemy import Column, Float, Integer, String

from app.models.db_base import Base


class FinanceSubsystem(Base):
    __tablename__ = "finance_subsystems"

    id = Column(Integer, primary_key=True, index=True)
    subsystem_name = Column(String(100), nullable=False, unique=True, index=True)
    planned_cost = Column(Float, nullable=False)
    actual_cost = Column(Float, nullable=False)
    labor_cost = Column(Float, nullable=False)
    material_cost = Column(Float, nullable=False)
    equipment_cost = Column(Float, nullable=False)