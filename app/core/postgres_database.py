from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

postgres_engine = create_engine(
    settings.postgres_url,
    echo=settings.db_echo,
    future=True
)

PostgresSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=postgres_engine
)


def get_postgres_db():
    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close()