"""Configuration for Whisper API."""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""

    api_host: str = "0.0.0.0"
    api_port: int = 5001
    log_level: str = "INFO"
    models_dir: Path = Path.home() / ".cache" / "huggingface" / "hub"

    class Config:
        env_prefix = "WHISPER_API_"
        case_sensitive = False


settings = Settings()
