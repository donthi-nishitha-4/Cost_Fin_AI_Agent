# Create a new file: tests/test_postgres_connection.py
from app.core.settings import settings
from sqlalchemy import create_engine, text

def test_connection():
    print(f"Attempting to connect to: {settings.postgres_url}")
    try:
        engine = create_engine(settings.postgres_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Successfully connected to PostgreSQL!")
            print(f"Result: {result.scalar()}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()