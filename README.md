# 🎙 Video/Audio Transcriber

動画・音声ファイルを文字起こしするツールです。英語・タガログ語に対応しています。

## 対応形式

MP3 / MP4 / MOV / M4A / WAV / AVI / MKV / AAC / FLAC

## セットアップ（Mac）

```bash
bash setup.sh
```

## 使い方

### かんたんモード（対話形式）

```bash
/usr/local/bin/python3.11 transcribe.py
```

ファイルパスや言語を対話形式で入力できます。

### コマンドラインモード

**1ファイルを文字起こし（英語）**
```bash
/usr/local/bin/python3.11 transcribe.py video.mp4
```

**タガログ語で文字起こし**
```bash
/usr/local/bin/python3.11 transcribe.py video.mp4 --language fil
```

**フォルダごと一括処理**
```bash
/usr/local/bin/python3.11 transcribe.py /path/to/folder --language en
```

**タイムスタンプ付きで出力**
```bash
/usr/local/bin/python3.11 transcribe.py video.mp4 --timestamps
```

**出力先フォルダを指定**
```bash
/usr/local/bin/python3.11 transcribe.py video.mp4 --output /path/to/output
```

## オプション

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--language` | `-l` | 言語 (`en` / `fil`) |
| `--model` | `-m` | モデルサイズ (`tiny` / `small` / `medium` / `large`) |
| `--timestamps` | `-t` | タイムスタンプを含める |
| `--output` | `-o` | 出力フォルダを指定 |

## 出力

元ファイルと同じ場所に `_transcript.txt` として保存されます。

## 必要環境

- macOS
- Python 3.11
- Homebrew
