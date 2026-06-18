from typing import Generator

from sqlalchemy.orm import Session #type:ignore

from app.core.database import SessionLocal


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_postgres_db_session() -> Generator[Session, None, None]:
    from app.core.postgres_database import PostgresSessionLocal

    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close()