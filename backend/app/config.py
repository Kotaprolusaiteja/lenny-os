from typing import Optional, List
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/lenny_os"
    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_timeout_seconds: float = 300.0
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-opus-20240229"
    embedding_provider: str = "local"
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_api_key: Optional[str] = None
    embedding_dimension: int = 384
    ollama_embedding_model: str = "all-minilm"
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["*"]
    log_level: str = "INFO"
    retrieval_top_k: int = 6
    chunk_size: int = 512
    chunk_overlap: int = 64

    @field_validator("database_url", mode="before")
    @classmethod
    def use_asyncpg_driver(cls, value: str) -> str:
        if value.startswith("postgres://"):
            value = value.replace("postgres://", "postgresql+asyncpg://", 1)
        if value.startswith("postgresql://"):
            value = value.replace("postgresql://", "postgresql+asyncpg://", 1)

        parsed = urlsplit(value)
        query = parse_qsl(parsed.query, keep_blank_values=True)
        query = [
            ("ssl" if key == "sslmode" else key, val)
            for key, val in query
            if key != "channel_binding"
        ]
        value = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))
        return value

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
