# JARVIS-Style AI Assistant Starter

This repository now includes a practical starter kit to help you build an AI assistant inspired by JARVIS.

## What this gives you

- A **local command-line assistant loop** (`jarvis.py`)
- A lightweight **tool system** (time, reminders, shell command execution)
- A clean foundation to add:
  - wake-word detection
  - speech-to-text (STT)
  - text-to-speech (TTS)
  - home automation integrations
  - calendar/email workflows

## Quick start

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Add OpenAI API key for LLM responses:

```bash
export OPENAI_API_KEY="your_key_here"
```

4. Run the assistant:

```bash
python jarvis.py
```

Type `help` to see built-in commands.

## Built-in commands

- `time` → current local time
- `remind <seconds> <message>` → sets a local timer reminder
- `run <shell command>` → runs a shell command safely (read-only intent; no sudo)
- `help` → command list
- `exit` / `quit` → stop

If a message is not a built-in command, the app will send it to OpenAI Chat Completions (if `OPENAI_API_KEY` is set).

## Suggested roadmap (to make it more “JARVIS-like”)

1. **Voice I/O**
   - STT: Whisper / faster-whisper
   - TTS: ElevenLabs / Coqui / pyttsx3
2. **Wake word**
   - Porcupine or openWakeWord
3. **Memory + context**
   - SQLite + vector search for long-term memory
4. **Tool integrations**
   - Calendar, email, smart home, IoT, notifications
5. **Automation brain**
   - Intent router + safety guardrails
6. **UI layer**
   - Web or desktop dashboard for logs, tasks, and control

## Security notes

- Never hardcode API keys.
- Keep a command allowlist for automation.
- Require confirmation for destructive actions.

---

If you want, the next step is I can help you add:
- voice input/output,
- wake-word activation,
- or a web dashboard.
