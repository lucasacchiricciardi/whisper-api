# Whisper API — Storico

## 2026-05-04

- **Creazione servizio**: nato dalla necessità di trascrizione audio per il TikTok Downloader. Ollama 0.22.1 non supporta `/api/transcribe`.
- **Architettura**: FastAPI + faster-whisper (CTranslate2), container Docker su server LLM, porta 5001.
- **GPU check**: nvidia-container-toolkit non presente (server AMD ROCm). GPU passata via `--device=/dev/kfd --device=/dev/dri` nel docker-compose.
- **Bug Dockerfile**: primo build falliva perché WORKDIR era `/app` ma i moduli Python stavano in `/app/app/`. Fix: aggiunto `WORKDIR /app/app` nel Dockerfile.
- **Bug model names**: primo tentativo usava `openai/whisper-small` (formato Transformers, non CTranslate2). Fix: cambiati a `Systran/faster-whisper-*` e `deepdml/faster-whisper-large-v3-turbo-ct2`.
- **Test superati**: small, medium, large-v3-turbo tutti funzionanti su file audio TikTok 53s in italiano.
- **CPU-only**: PyTorch CUDA build nel container non vede GPU AMD. Service gira su CPU/int8. Da ottimizzare.
- **Pulizia Ollama**: rimossi 3 modelli Whisper GGUF (oxide-lab small/medium, xkeyC large-v3-turbo) da Ollama — ~1.1GB liberati.
- **Gitea**: repo `LogWhispererAI/whisper-api` creato, codice pushato.
- **Registry**: immagine `192.168.254.150:5000/whisper-api:latest` pushata.
- **TikTok Downloader aggiornato**: transcriber.py, config.py, main.py modificati per chiamare Whisper API.
