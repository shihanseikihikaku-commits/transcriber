# 🎙 Video/Audio Transcriber

A transcription tool for video and audio files. Supports English and Tagalog.

## Supported Formats

MP3 / MP4 / MOV / M4A / WAV / AVI / MKV / AAC / FLAC

## Requirements

- Python 3.11+
- ffmpeg
- whisper-ctranslate2

---

## Setup

### Mac

```bash
bash setup.sh
```

Or manually:

```bash
brew install python@3.11 ffmpeg
pip3 install whisper-ctranslate2
```

### Windows

1. Install [Python 3.11](https://www.python.org/downloads/)
2. Install [ffmpeg](https://ffmpeg.org/download.html) and add it to PATH
3. Open Command Prompt and run:

```bash
pip install whisper-ctranslate2
```

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
pip3 install whisper-ctranslate2
```

---

## Usage

### Interactive Mode

```bash
python3 transcribe.py
```

Follow the prompts to select a file and language.

### Command Line Mode

**Transcribe a single file (English)**
```bash
python3 transcribe.py video.mp4
```

**Transcribe in Tagalog**
```bash
python3 transcribe.py video.mp4 --language fil
```

**Batch process a folder**
```bash
python3 transcribe.py /path/to/folder --language en
```

**Include timestamps**
```bash
python3 transcribe.py video.mp4 --timestamps
```

**Specify output folder**
```bash
python3 transcribe.py video.mp4 --output /path/to/output
```

---

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--language` | `-l` | Language (`en` for English / `fil` for Tagalog) |
| `--model` | `-m` | Model size (`tiny` / `small` / `medium` / `large`) |
| `--timestamps` | `-t` | Include timestamps in output |
| `--output` | `-o` | Output folder path |

## Output

Transcripts are saved as `_transcript.txt` in the same folder as the source file.

---

## Notes

- The first run will download the Whisper model (a few hundred MB).
- Larger models (`medium`, `large`) are more accurate but slower.
- Internet connection is only required for the initial model download.
