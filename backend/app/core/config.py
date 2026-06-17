from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Bajirao AI Portfolio API"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "bajirao_ai_portfolio"
    db_user: str = "postgres"
    db_password: SecretStr

    database_url: str | None = None
    
    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    github_username: str = "Bajirao-99"
    github_api_version: str = "2026-03-10"
    github_token: SecretStr | None = None

    embedding_model_name: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    disable_embedding_model: bool = False

    gemini_api_key: SecretStr
    gemini_model_name: str = "gemini-3.5-flash"

    chat_retrieval_top_k: int = 6
    chat_min_relevance_score: float = 0.12
    chat_rate_limit: int = 10
    chat_rate_window_minutes: int = 10

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # app_env: str = "development"
    # debug: bool = False
    enable_docs: bool = True
    log_level: str = "INFO"

    cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    )

    trusted_hosts: str = (
        "localhost,127.0.0.1"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    @property
    def trusted_hosts_list(self) -> list[str]:
        return [
            host.strip()
            for host in self.trusted_hosts.split(",")
            if host.strip()
        ]

settings = Settings()