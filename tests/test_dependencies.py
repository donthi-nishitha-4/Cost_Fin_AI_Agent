from app.core.dependencies import get_db_session, get_postgres_db_session


def test_get_db_session_yields_a_session():
    generator = get_db_session()

    try:
        db = next(generator)
        assert db is not None
    finally:
        generator.close()


def test_get_postgres_db_session_returns_a_generator():
    generator = get_postgres_db_session()

    try:
        assert generator is not None
    finally:
        generator.close()
