# Whisper API

REST API service for audio transcription using Whisper (faster-whisper + CTranslate2).

## Overview

Whisper API provides a simple HTTP interface for transcribing audio files using OpenAI's Whisper model via the `faster-whisper` library. It supports lazy loading of models and exposes endpoints for transcription, model management, and health checks.

## Features

- **REST API** for audio transcription (MP3, WAV, M4A)
- **Lazy model loading** — models are loaded on first use
- **Multiple models**: tiny, base, small, medium, large-v3, large-v3-turbo
- **Language auto-detection** with optional override
- **Initial prompt support** for context-aware transcription
- **Model lifecycle management** — load, unload, list available models
- **Health check endpoints** for monitoring
- **Docker containerization** for easy deployment

## API Endpoints

### Transcription

```http
POST /transcribe
Content-Type: multipart/form-data

Parameters:
  - audio (file, required): Audio file (MP3, WAV, M4A)
  - model (string, optional): Model size (default: "medium")
    Choices: tiny, base, small, medium, large-v3, large-v3-turbo
  - language (string, optional): Language code (e.g., "it", "en")
  - initial_prompt (string, optional): Initial prompt for context

Response (200 OK):
{
  "text": "transcribed text",
  "language": "it",
  "language_probability": 0.95,
  "duration_sec": 23.5,
  "model": "medium"
}
```

### Model Management

```http
GET /models
Response: { "available": ["tiny", "base", ...], "loaded": ["medium"] }

POST /models/load?model=large-v3
Response: { "status": "loaded", "model": "large-v3" }

POST /models/unload?model=medium
Response: { "status": "unloaded" }
```

### Health

```http
GET /health
Response: { "status": "ok" }

GET /status
Response: { "uptime_sec": 3600, "loaded_models": ["medium"], ... }
```

## Requirements

- Python 3.10+
- FFmpeg (for audio conversion)
- 8 GB+ RAM (depends on model size)
- Optional: GPU with ROCm or CUDA support

## Installation

### Docker (Recommended)

```bash
docker-compose up -d
```

The service will be available at `http://localhost:5001`.

### Local Installation

```bash
pip install -r requirements.txt
python app/main.py
```

## Configuration

Environment variables:

- `WHISPER_API_HOST`: Server host (default: `0.0.0.0`)
- `WHISPER_API_PORT`: Server port (default: `5001`)
- `MODELS_DIR`: Directory for model cache (default: `~/.cache/huggingface/hub`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## Usage Examples

### Python

```python
import httpx
from pathlib import Path

with open("audio.mp3", "rb") as f:
    r = httpx.post(
        "http://localhost:5001/transcribe",
        files={"audio": ("audio.mp3", f)},
        data={
            "model": "medium",
            "language": "it",
            "initial_prompt": "Technical discussion about AI"
        }
    )
result = r.json()
print(result["text"])
```

### cURL

```bash
curl -X POST http://localhost:5001/transcribe \
  -F "audio=@audio.mp3" \
  -F "model=medium" \
  -F "language=it"
```

## Performance

Typical transcription times (on CPU):

| Model | Size | ~60s audio | ~600s audio |
|-------|------|-----------|-----------|
| tiny | ~40 MB | 2-3s | 15-20s |
| small | ~46 MB | 8-12s | 60-90s |
| medium | ~150 MB | 20-30s | 200-300s |
| large-v3 | ~2.7 GB | 60-90s | 600-900s |
| large-v3-turbo | ~1.5 GB | 40-60s | 400-600s |

With GPU (ROCm/CUDA): 2-5x faster.

## Architecture

```
HTTP Request → FastAPI → transcribe() → faster-whisper
                ↓
             Model cache (lazy load)
```

## Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format & lint
black app/ && flake8 app/

# Type checking
mypy app/
```

## License

MIT License — see [LICENSE](LICENSE)

## Related Projects

- [faster-whisper](https://github.com/guillaumekln/faster-whisper) — Fast Whisper inference
- [OpenAI Whisper](https://github.com/openai/whisper) — Original Whisper model
- [TikTok Downloader](https://github.com/lucasacchiricciardi/tiktok-downloader) — Consumer of this API
- [Shortcutter](https://github.com/lucasacchiricciardi/shortcutter) — Consumer of this API
