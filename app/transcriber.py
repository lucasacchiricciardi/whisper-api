"""Audio transcription module."""

import time
from pathlib import Path
from typing import Optional

from faster_whisper import WhisperModel


class Transcriber:
    """Whisper transcriber with model caching."""

    def __init__(self, models_dir: Path | str | None = None):
        """Initialize transcriber."""
        self.models_cache: dict[str, WhisperModel] = {}
        self.models_dir = models_dir

    def get_model(self, model_size: str) -> WhisperModel:
        """Get or load a model."""
        if model_size not in self.models_cache:
            self.models_cache[model_size] = WhisperModel(
                model_size,
                device="cpu",
                compute_type="int8",
                download_root=str(self.models_dir) if self.models_dir else None,
            )
        return self.models_cache[model_size]

    def transcribe(
        self,
        audio_path: Path | str,
        model_size: str = "medium",
        language: Optional[str] = None,
        initial_prompt: Optional[str] = None,
    ) -> dict:
        """Transcribe audio file."""
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        t0 = time.time()
        model = self.get_model(model_size)

        segments, info = model.transcribe(
            str(audio_path),
            language=language,
            beam_size=5,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
            initial_prompt=initial_prompt,
        )

        transcript = " ".join(seg.text.strip() for seg in segments).strip()
        elapsed = time.time() - t0

        return {
            "text": transcript,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration_sec": round(elapsed, 2),
            "model": model_size,
        }

    def get_loaded_models(self) -> list[str]:
        """Get list of loaded models."""
        return list(self.models_cache.keys())

    def unload_model(self, model_size: str) -> None:
        """Unload a model."""
        if model_size in self.models_cache:
            del self.models_cache[model_size]

    def unload_all(self) -> None:
        """Unload all models."""
        self.models_cache.clear()
