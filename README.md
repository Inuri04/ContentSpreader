# KI-Content-Veredler

Eine einfache Web-Anwendung, die aus einem hochgeladenen Video automatisch Social-Media-Beiträge generiert.

## Funktionen
- **Video-Upload** mit Extraktion der Tonspur und Transkription via [OpenAI Whisper](https://github.com/openai/whisper)
- **Abstrakte Zusammenfassung** der Transkription mit Hilfe von Transformer-Modellen
- **Post-Generator** für LinkedIn, einen nummerierten Twitter-Thread und einen Newsletter-Text
- **Ausgabe** der generierten Texte im Browser mit Kopierfunktion

## Installation
1. Python 3.9+ installieren.
2. Abhängigkeiten installieren:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Zusätzlich wird [FFmpeg](https://ffmpeg.org/) benötigt, z. B. unter Ubuntu:
   ```bash
   sudo apt-get install ffmpeg
   ```

## Starten der Anwendung
```bash
uvicorn app.main:app --reload
```
Danach im Browser `http://localhost:8000` aufrufen, ein Video hochladen und die generierten Inhalte nutzen.

## Hinweise
- Modelle für Whisper und Transformer werden beim ersten Start automatisch heruntergeladen und benötigen entsprechend Zeit und Speicher.
- Die Anwendung dient als Demo und wurde nicht für den produktiven Einsatz optimiert.
