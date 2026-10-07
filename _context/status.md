# Whisper API — Status

categoria: infra

## Stato
🟢 OPERATIVO — servizio attivo su 192.168.254.115:5001, trascrizione testata con 3 modelli (small, medium, large-v3-turbo).
✅ Repository GitHub public (MIT license): https://github.com/lucasacchiricciardi/whisper-api
⚠️ **Dal 2026-10-07 questo repo non è il codice in produzione.** Su llm gira `LogWhispererAI/whisper-api` (Gitea),
che ha un'altra storia e il modello `parakeet`; questo repo è rimasto alla versione di maggio. Quale dei due tenere è
una decisione aperta (INV-0087 nel workspace).

## Deploy
- **Host**: server LLM (192.168.254.115) — `/opt/whisper-api/`
- **Container**: `whisper-api` (network_mode: host)
- **Immagine**: `whisper-api-whisper-api`, costruita su llm con `docker compose build` (non dal registry)
- **Gitea**: `LogWhispererAI/whisper-api` (branch main, privato)

## Modelli testati
| Modello | Dimensione | Qualità | Lingua |
|---|---|---|---|
| small (Systran) | ~46MB | Buona, punteggiatura approssimativa | IT 99.55% |
| medium (Systran) | ~150MB | Ottima, punteggiatura corretta | IT 99.4% |
| large-v3-turbo (deepdml) | ~1.5GB | Ottima, termini tecnici precisi | IT 99.84% |
| **parakeet** (Parakeet TDT 0.6B v3, ONNX int8) | ~0.7GB | Meno errori sui nomi propri di `medium`, numeri in lettere | 25 lingue europee, riconoscimento automatico |

Dal 2026-10-07 `parakeet` è il modello usato da tutti i chiamanti: sulla CPU di llm è 3,8-4,2 volte più veloce di
`medium` e non salta parlato su un file di 57 minuti (misura con criteri fissati prima, nel workspace:
`projects/inventario/stt-cpu-misura-2026-10-07.md`).

## Prossima azione
1. ~~Valutare accelerazione GPU ROCm~~ — **provata e scartata il 2026-10-07**: con la wheel ROCm ufficiale di CTranslate2 4.8.2 sulla 7900 XTX il modello si carica ma produce testo sbagliato, e un tipo di calcolo dà un fault della GPU, condivisa con llama-swap. Si resta su CPU, con `parakeet`.
2. Aggiungere autenticazione API (token bearer) se esposto fuori LAN
3. Valutare auto-unload modelli dopo timeout di inattività
4. **Documentare pattern chunked transcription** in README (ffmpeg split + loop sequenziale) — necessario per file > 1h su CPU
5. **Valutare timeout/health-check più aggressivi** sul container (oggi server resta "Up" anche se servizio è freezed)

## Note tecniche
- Il container gira su **CPU** (int8) perché PyTorch nel container è build CUDA e non vede la GPU AMD
- Per la GPU non basta PyTorch ROCm: faster-whisper usa CTranslate2, e la sua build ROCm su questa scheda dà output sbagliato (2026-10-07)
- Modelli scaricati da HuggingFace: Systran/faster-whisper-* e deepdml/faster-whisper-large-v3-turbo-ct2
- I modelli Whisper GGUF sono stati rimossi da Ollama (inutili)

## Ultimo aggiornamento
2026-10-07 — su CPU per scelta, modello `parakeet` in produzione; la GPU è scartata. Questo repo diverge da quello in produzione (INV-0087).

## Status aggiunto per contesto
- ✅ Servizio operativo 192.168.254.115:5001 (CPU-based, latenza accettabile per ora)
- ⛔ GPU ROCm acceleration: scartata il 2026-10-07 (output sbagliato e fault della GPU). Il guadagno di velocità è arrivato da `parakeet` su CPU
- 🔲 Documentazione chunked transcription pattern (ffmpeg split + loop sequenziale per file >1h)
