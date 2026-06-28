from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

engine = create_engine(
    settings.database_url,
    pool_size=10,  # Increased connection pool size for better performance
    max_overflow=50,  # Allow more connections under load
    pool_timeout=30,
    echo=settings.db_echo,
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()