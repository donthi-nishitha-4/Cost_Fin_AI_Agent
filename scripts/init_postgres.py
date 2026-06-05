from app.core.postgres_database import postgres_engine, PostgresSessionLocal
from app.core.seed_database import seed_finance_database
from app.models.db_base import Base


def main():
    Base.metadata.create_all(bind=postgres_engine)

    db = PostgresSessionLocal()
    try:
        seed_finance_database(db)
    finally:
        db.close()

    print("PostgreSQL database initialized and seeded.")


if __name__ == "__main__":
    main()