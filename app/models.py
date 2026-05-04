"""Data models for Whisper API."""

from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    """Transcription request body."""

    model: str = "medium"
    language: str | None = None
    initial_prompt: str | None = None


class TranscriptionResponse(BaseModel):
    """Transcription response."""

    text: str
    language: str
    language_probability: float
    duration_sec: float
    model: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str


class ModelsResponse(BaseModel):
    """Available models response."""

    available: list[str]
    loaded: list[str]
