"""Whisper API service."""

import logging
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse

from app import __version__
from app.config import settings
from app.models import TranscriptionResponse, HealthResponse, ModelsResponse
from app.transcriber import Transcriber

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Initialize app
app = FastAPI(
    title="Whisper API",
    description="REST API for audio transcription using Whisper",
    version=__version__,
)

# Initialize transcriber
transcriber = Transcriber(models_dir=settings.models_dir)

# Supported models
SUPPORTED_MODELS = ["tiny", "base", "small", "medium", "large-v3", "large-v3-turbo"]


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/status")
async def status():
    """Service status endpoint."""
    return {
        "status": "ok",
        "version": __version__,
        "loaded_models": transcriber.get_loaded_models(),
        "supported_models": SUPPORTED_MODELS,
    }


@app.get("/models", response_model=ModelsResponse)
async def list_models():
    """List available and loaded models."""
    return {
        "available": SUPPORTED_MODELS,
        "loaded": transcriber.get_loaded_models(),
    }


@app.post("/models/load")
async def load_model(model: str):
    """Load a model into memory."""
    if model not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model: {model}. Choose from: {SUPPORTED_MODELS}",
        )
    try:
        transcriber.get_model(model)
        return {"status": "loaded", "model": model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")


@app.post("/models/unload")
async def unload_model(model: str):
    """Unload a model from memory."""
    try:
        transcriber.unload_model(model)
        return {"status": "unloaded", "model": model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unload model: {str(e)}")


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(
    audio: UploadFile,
    model: str = Form(default="medium"),
    language: str = Form(default=""),
    initial_prompt: str = Form(default=""),
):
    """Transcribe audio file."""
    if model not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model: {model}. Choose from: {SUPPORTED_MODELS}",
        )

    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".audio") as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = transcriber.transcribe(
            tmp_path,
            model_size=model,
            language=language or None,
            initial_prompt=initial_prompt or None,
        )
        return TranscriptionResponse(**result)
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        # Clean up temporary file
        Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
