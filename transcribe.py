#!/usr/bin/env python3
"""
Video/Audio Transcriber using Whisper
Supports English and Tagalog
"""

import subprocess
import sys
import os
import argparse

SUPPORTED_EXTENSIONS = {'.mp3', '.mp4', '.mov', '.m4a', '.wav', '.avi', '.mkv', '.aac', '.flac'}
LANGUAGES = {
    'en': 'English',
    'fil': 'Tagalog',
}


def transcribe_file(file_path, language='en', model='small', with_timestamps=False):
    """Transcribe a single audio/video file."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        print(f'スキップ: 未対応の形式 {file_path}')
        return None

    print(f'\n処理中: {os.path.basename(file_path)}')
    print(f'言語: {LANGUAGES.get(language, language)} / モデル: {model}')

    result = subprocess.run(
        ['whisper-ctranslate2', file_path, '--language', language, '--model', model],
        capture_output=True, text=True
    )

    raw_output = result.stdout or result.stderr
    if not raw_output.strip():
        print('エラー: 出力が取得できませんでした')
        return None

    # タイムスタンプなしのテキストを抽出
    lines = []
    for line in raw_output.splitlines():
        line = line.strip()
        if not line:
            continue
        if with_timestamps:
            lines.append(line)
        else:
            # "[00:00.000 --> 00:04.000]  text" からテキスト部分だけ取り出す
            if '-->' in line:
                text = line.split(']', 1)[-1].strip()
                if text:
                    lines.append(text)
            else:
                lines.append(line)

    return '\n'.join(lines)


def save_transcript(file_path, content, output_dir=None):
    """Save transcript as a text file."""
    base = os.path.splitext(file_path)[0]
    if output_dir:
        base = os.path.join(output_dir, os.path.basename(base))
    out_path = base + '_transcript.txt'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'保存: {out_path}')
    return out_path


def process_folder(folder_path, language='en', model='small', with_timestamps=False, output_dir=None):
    """Process all supported files in a folder."""
    files = [
        os.path.join(folder_path, f)
        for f in sorted(os.listdir(folder_path))
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]
    if not files:
        print('対応ファイルが見つかりませんでした')
        return

    print(f'{len(files)}件のファイルを処理します')
    for file_path in files:
        content = transcribe_file(file_path, language, model, with_timestamps)
        if content:
            save_transcript(file_path, content, output_dir)


def interactive_mode():
    """Run in interactive mode when no arguments are provided."""
    print('=== 文字起こしツール ===')
    print()

    # ファイルかフォルダか
    target = input('ファイルまたはフォルダのパスを入力（ドラッグ＆ドロップも可）: ').strip().strip("'\"")

    if not os.path.exists(target):
        print('エラー: パスが見つかりません')
        sys.exit(1)

    # 言語選択
    print()
    print('言語を選択してください:')
    print('  1. 英語 (en)')
    print('  2. タガログ語 (fil)')
    lang_choice = input('番号を入力 [1]: ').strip() or '1'
    language = 'fil' if lang_choice == '2' else 'en'

    # タイムスタンプ
    print()
    ts_choice = input('タイムスタンプを含める？ (y/N): ').strip().lower()
    with_timestamps = ts_choice == 'y'

    print()

    if os.path.isdir(target):
        process_folder(target, language, with_timestamps=with_timestamps)
    else:
        content = transcribe_file(target, language, with_timestamps=with_timestamps)
        if content:
            save_transcript(target, content)

    print('\n完了しました！')


def main():
    parser = argparse.ArgumentParser(description='動画・音声ファイルの文字起こしツール')
    parser.add_argument('target', nargs='?', help='ファイルまたはフォルダのパス')
    parser.add_argument('--language', '-l', choices=['en', 'fil'], default='en', help='言語 (en/fil)')
    parser.add_argument('--model', '-m', default='small', help='モデルサイズ (tiny/small/medium/large)')
    parser.add_argument('--timestamps', '-t', action='store_true', help='タイムスタンプを含める')
    parser.add_argument('--output', '-o', help='出力フォルダ（省略時は元ファイルと同じ場所）')

    args = parser.parse_args()

    if not args.target:
        interactive_mode()
        return

    target = args.target
    if not os.path.exists(target):
        print(f'エラー: {target} が見つかりません')
        sys.exit(1)

    if os.path.isdir(target):
        process_folder(target, args.language, args.model, args.timestamps, args.output)
    else:
        content = transcribe_file(target, args.language, args.model, args.timestamps)
        if content:
            save_transcript(target, content, args.output)

    print('\n完了しました！')


if __name__ == '__main__':
    main()
