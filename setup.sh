#!/bin/bash
echo "=== 文字起こしツール セットアップ ==="
echo ""

# Homebrewの確認
if ! command -v brew &>/dev/null; then
    echo "Homebrewをインストールしてください: https://brew.sh"
    exit 1
fi

# Python 3.11の確認・インストール
if ! command -v /usr/local/bin/python3.11 &>/dev/null; then
    echo "Python 3.11をインストール中..."
    brew install python@3.11
fi

# ffmpegの確認・インストール
if ! command -v ffmpeg &>/dev/null; then
    echo "ffmpegをインストール中..."
    brew install ffmpeg
fi

# Whisperのインストール
echo "Whisperをインストール中..."
/usr/local/bin/python3.11 -m pip install whisper-ctranslate2

echo ""
echo "セットアップ完了！"
echo "使い方: /usr/local/bin/python3.11 transcribe.py"
