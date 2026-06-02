from app.core.database import engine
from app.core.seed_database import seed_finance_database
from app.models.db_base import Base


def main():
    Base.metadata.create_all(bind=engine)
    seed_finance_database()
    print("Database initialized and seeded.")


if __name__ == "__main__":
    main()