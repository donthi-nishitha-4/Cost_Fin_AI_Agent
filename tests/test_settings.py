from app.core.settings import settings


def test_settings_expose_database_configuration():
    assert settings.project_name == "Cost Finance AI Agent"
    assert settings.environment == "development"
    assert settings.log_level == "DEBUG"
    assert settings.llm_model == "llama3"
    assert settings.database_url == (
        "postgresql+psycopg://postgres:postgres@localhost:5432/cost_finance"
    )
    assert settings.db_echo is False
    assert settings.postgres_url == (
        "postgresql+psycopg://postgres:postgres@localhost:5432/cost_finance"
    )
