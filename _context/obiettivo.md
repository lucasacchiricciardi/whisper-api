# Whisper API — Obiettivo

Servizio REST sempre attivo per la trascrizione audio tramite Whisper (faster-whisper + CTranslate2). Espone una API HTTP che qualsiasi client può chiamare (TikTok Downloader, n8n, skill Claude, altri agenti).

## Requisiti

- Trascrizione audio MP3/WAV/M4A con Whisper
- Modelli: tiny, base, small, medium, large-v3, large-v3-turbo
- Lazy loading dei modelli (caricati alla prima richiesta)
- Endpoints: /transcribe, /models, /health, /status, /models/load, /models/unload
- Container Docker, network_mode: host, restart: unless-stopped
- GPU passthrough per ROCm (device /dev/kfd + /dev/dri)

## Contesto

Nato perché Ollama 0.22.1 non supporta l'endpoint `/api/transcribe` per audio. Il TikTok Downloader aveva bisogno di trascrivere audio ma Ollama è text-in/text-out. faster-whisper è la stessa libreria usata da Shortcutter.
