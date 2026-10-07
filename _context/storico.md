# Whisper API — Storico

## 2026-10-07

- **La GPU è scartata**: il container girava su CPU senza dirlo (torch CUDA, ctranslate2 senza HIP). La wheel ROCm
  ufficiale di CTranslate2 4.8.2 sulla 7900 XTX carica il modello ma produce testo sbagliato; `int8_float16` dà un fault
  della GPU, che è condivisa con llama-swap. Decisione di Luca: si resta su CPU.
- **Arriva `parakeet`** (Parakeet TDT 0.6B v3, ONNX int8 solo pesi), misurato contro `medium` con criteri fissati prima:
  3,8-4,2 volte più veloce, nessun parlato saltato su 57 minuti, meno errori sui nomi propri. In produzione e usato da
  tutti i chiamanti.
- ⚠️ Quelle modifiche stanno nel repo Gitea `LogWhispererAI/whisper-api`, che è il codice in esercizio. Questo repo
  GitHub ha un'altra storia ed è rimasto a maggio: quale tenere è aperto (INV-0087 nel workspace).

## 2026-05-13

- **Overload con file grossi su CPU**: tentativo trascrizione MP3 di 2h 49m (corso Beggiato Claude Code, 201 MB) con modello `medium` → server **bloccato** dopo ~10 min, nessun output, container ancora "Up" ma servizio non risponde.
- **Reboot server llm**: dopo blocco, reboot completo del server llm (192.168.254.115). Servizi tornati online in ~30 sec.
- **Pattern chunked transcription**: per file > 1h va splittato con `ffmpeg -f segment -segment_time 1800 -c copy` (segmenti da 30 min, no re-encode). Trascrizione sequenziale di ogni chunk via `curl http://127.0.0.1:5001/transcribe?model=small` (chiamata localhost dal server, no network overhead). Concatenazione finale dei campi `text` dei JSON.
- **Lesson SIGHUP**: lanciare loop bash via `ssh remote "for chunk in ...; do curl ...; done"` viene killato da SIGHUP alla chiusura SSH. Soluzione: `nohup bash -c '...' </dev/null > /dev/null 2>&1 & disown`.
- **Trascrizione corso Beggiato** in corso: 6 chunks da 30 min, modello `small`, in `/tmp/corso-trans/` su llm. Lanciata 2026-05-13 12:05 CEST, ETA 12:55 CEST.

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
