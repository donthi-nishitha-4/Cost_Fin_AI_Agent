from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = Field(default="Cost Finance AI Agent")
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")
    llm_model: str = Field(default="llama3")
    database_url: str = Field(default="sqlite:///./finance.db")
    db_echo: bool = Field(default=False)

    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="cost_finance")
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    postgres_driver: str = Field(default="postgresql+psycopg")

    @property
    def postgres_url(self) -> str:
        return (
            f"{self.postgres_driver}://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()