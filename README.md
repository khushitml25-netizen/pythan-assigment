# English Dictionary App

This is a desktop Python application built with Tkinter. It searches the Dictionary API, falls back to local offline definitions, supports speech output, and stores search history in a local `history.txt` file.

## Requirements

- Python 3.10+
- Windows (recommended, because `pyttsx3` uses the Windows speech engine)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run the app

```bash
python "python dictionary(phase 2).py"
```

## Build a Windows executable

```bash
pyinstaller --onefile --windowed --name "EnglishDictionary" "python dictionary(phase 2).py"
```

This creates a bundled `.exe` in the `dist/` folder.

## Notes

- The app writes `history.txt` in the current working directory.
- If the online dictionary API is unavailable, the app uses built-in offline word data.
- The speech feature requires a working Windows TTS voice.
