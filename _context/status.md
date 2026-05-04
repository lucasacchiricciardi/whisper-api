# Whisper API — Status

## Stato
🟢 OPERATIVO — servizio attivo su 192.168.254.115:5001, trascrizione testata con 3 modelli (small, medium, large-v3-turbo).
✅ Repository GitHub public (MIT license): https://github.com/lucasacchiricciardi/whisper-api

## Deploy
- **Host**: server LLM (192.168.254.115) — `/opt/whisper-api/`
- **Container**: `whisper-api` (network_mode: host)
- **Registro**: `192.168.254.150:5000/whisper-api:latest`
- **Gitea**: `LogWhispererAI/whisper-api` (branch main, privato)

## Modelli testati
| Modello | Dimensione | Qualità | Lingua |
|---|---|---|---|
| small (Systran) | ~46MB | Buona, punteggiatura approssimativa | IT 99.55% |
| medium (Systran) | ~150MB | Ottima, punteggiatura corretta | IT 99.4% |
| large-v3-turbo (deepdml) | ~1.5GB | Ottima, termini tecnici precisi | IT 99.84% |

## Prossima azione
1. Valutare accelerazione GPU ROCm (attualmente gira su CPU/int8)
2. Aggiungere autenticazione API (token bearer) se esposto fuori LAN
3. Valutare auto-unload modelli dopo timeout di inattività

## Note tecniche
- Il container gira su **CPU** (int8) perché PyTorch nel container è build CUDA e non vede la GPU AMD
- Per abilitare GPU: usare PyTorch ROCm build (`--index-url https://download.pytorch.org/whl/rocm6.2`)
- Modelli scaricati da HuggingFace: Systran/faster-whisper-* e deepdml/faster-whisper-large-v3-turbo-ct2
- I modelli Whisper GGUF sono stati rimossi da Ollama (inutili)

## Ultimo aggiornamento
2026-05-04
