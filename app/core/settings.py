from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = Field(default="Cost Finance AI Agent")
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")
    llm_model: str = Field(default="llama3")
    database_url: str = Field(default="sqlite:///./finance.db")
    db_echo: bool = Field(default=False)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()