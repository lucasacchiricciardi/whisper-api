# Whisper API — Relazioni con altri progetti

## TikTok Downloader

Relazione **service→consumer**. Il TikTok Downloader chiama `POST /transcribe` su `192.168.254.115:5001` per trascrizione audio. Prima chiamava Ollama `/api/transcribe` che non esiste.

## Shortcutter

Relazione **fratello**. Shortcutter usa `faster-whisper` direttamente (non via API). Whisper API ne è la versione "servicizzata". Stessa libreria, stesso approccio (VAD filter, beam_size=5, initial_prompt).

## Model Manager

Relazione **gemello architetturale**. Stesso pattern: container Docker slim, FastAPI, network_mode: host, restart unless-stopped. Model Manager gestisce il lifecycle dei modelli LLM su Ollama; Whisper API gestisce il lifecycle dei modelli Whisper autonomamente.

## TwinScribeAI

Relazione **service→consumer futuro**. Quando TwinScribeAI sarà operativo, può usare Whisper API come backend di trascrizione al posto di faster-whisper embedded.

## LogWhispererAI

Relazione **indiretta**. LogWhispererAI potrebbe usare Whisper API per trascrizione di log vocali o note audio in futuro.

## Infrastruttura

| Componente | Indirizzo | Note |
|---|---|---|
| Whisper API | 192.168.254.115:5001 | Porta 5001 |
| Server LLM | 192.168.254.115 | Host del container |
| Docker registry | 192.168.254.150:5000 | `whisper-api:latest` |
| Gitea | gitea.lab.home.lucasacchi.net | `LogWhispererAI/whisper-api` |
