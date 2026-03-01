#!/usr/bin/env python3
"""
Video/Audio Transcriber - GUI Version
Supports English and Tagalog
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys

SUPPORTED_EXTENSIONS = {'.mp3', '.mp4', '.mov', '.m4a', '.wav', '.avi', '.mkv', '.aac', '.flac'}


def transcribe_file(file_path, language, with_timestamps, log_callback):
    from faster_whisper import WhisperModel

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        log_callback(f'Skipped (unsupported format): {os.path.basename(file_path)}')
        return None

    log_callback(f'Processing: {os.path.basename(file_path)}')
    log_callback('Loading model... (first time may take a while)')

    model = WhisperModel('tiny', device='cpu', compute_type='int8')

    log_callback('Transcribing...')
    segments, info = model.transcribe(file_path, language=language)

    lines = []
    for segment in segments:
        if with_timestamps:
            lines.append(f'[{segment.start:.2f}s --> {segment.end:.2f}s]  {segment.text.strip()}')
        else:
            lines.append(segment.text.strip())

    return '\n'.join(lines)


def save_transcript(file_path, content):
    out_path = os.path.splitext(file_path)[0] + '_transcript.txt'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return out_path


class TranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title('🎙 Video/Audio Transcriber')
        self.root.geometry('560x480')
        self.root.resizable(False, False)
        self.root.configure(bg='#1e1e2e')

        self.files = []
        self.running = False

        self._build_ui()

    def _build_ui(self):
        tk.Label(
            self.root, text='🎙 Video / Audio Transcriber',
            font=('Helvetica', 16, 'bold'), bg='#1e1e2e', fg='#cdd6f4'
        ).pack(pady=(24, 4))

        tk.Label(
            self.root, text='Supports English and Tagalog',
            font=('Helvetica', 11), bg='#1e1e2e', fg='#6c7086'
        ).pack()

        file_frame = tk.Frame(self.root, bg='#1e1e2e')
        file_frame.pack(pady=16, padx=24, fill='x')

        tk.Button(
            file_frame, text='Select Files',
            command=self.select_files,
            bg='#89b4fa', fg='#1e1e2e', font=('Helvetica', 12, 'bold'),
            relief='flat', padx=16, pady=8, cursor='hand2'
        ).pack(side='left')

        tk.Button(
            file_frame, text='Select Folder',
            command=self.select_folder,
            bg='#313244', fg='#cdd6f4', font=('Helvetica', 12),
            relief='flat', padx=16, pady=8, cursor='hand2'
        ).pack(side='left', padx=(8, 0))

        self.file_label = tk.Label(
            file_frame, text='No files selected',
            font=('Helvetica', 11), bg='#1e1e2e', fg='#6c7086'
        )
        self.file_label.pack(side='left', padx=12)

        lang_frame = tk.Frame(self.root, bg='#1e1e2e')
        lang_frame.pack(pady=4, padx=24, fill='x')

        tk.Label(
            lang_frame, text='Language:',
            font=('Helvetica', 12), bg='#1e1e2e', fg='#cdd6f4'
        ).pack(side='left')

        self.lang_var = tk.StringVar(value='en')
        tk.Radiobutton(
            lang_frame, text='English', variable=self.lang_var, value='en',
            bg='#1e1e2e', fg='#cdd6f4', selectcolor='#313244',
            activebackground='#1e1e2e', font=('Helvetica', 12)
        ).pack(side='left', padx=(12, 0))
        tk.Radiobutton(
            lang_frame, text='Tagalog', variable=self.lang_var, value='fil',
            bg='#1e1e2e', fg='#cdd6f4', selectcolor='#313244',
            activebackground='#1e1e2e', font=('Helvetica', 12)
        ).pack(side='left', padx=(8, 0))

        ts_frame = tk.Frame(self.root, bg='#1e1e2e')
        ts_frame.pack(pady=4, padx=24, fill='x')

        self.ts_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            ts_frame, text='Include timestamps',
            variable=self.ts_var,
            bg='#1e1e2e', fg='#cdd6f4', selectcolor='#313244',
            activebackground='#1e1e2e', font=('Helvetica', 12)
        ).pack(side='left')

        self.start_btn = tk.Button(
            self.root, text='Start Transcription',
            command=self.start_transcription,
            bg='#a6e3a1', fg='#1e1e2e', font=('Helvetica', 13, 'bold'),
            relief='flat', padx=24, pady=10, cursor='hand2'
        )
        self.start_btn.pack(pady=16)

        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=500)
        self.progress.pack(pady=(0, 8))

        log_frame = tk.Frame(self.root, bg='#1e1e2e')
        log_frame.pack(padx=24, fill='both', expand=True, pady=(0, 20))

        self.log_text = tk.Text(
            log_frame, height=8, bg='#181825', fg='#a6e3a1',
            font=('Courier', 11), relief='flat', wrap='word',
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title='Select video/audio files',
            filetypes=[('Media files', '*.mp3 *.mp4 *.mov *.m4a *.wav *.avi *.mkv *.aac *.flac')]
        )
        if files:
            self.files = list(files)
            self.file_label.config(text=f'{len(self.files)} file(s) selected')

    def select_folder(self):
        folder = filedialog.askdirectory(title='Select folder')
        if folder:
            self.files = [
                os.path.join(folder, f) for f in sorted(os.listdir(folder))
                if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
            ]
            self.file_label.config(text=f'{len(self.files)} file(s) found in folder')

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def start_transcription(self):
        if not self.files:
            messagebox.showwarning('No files', 'Please select files or a folder first.')
            return
        if self.running:
            return

        self.running = True
        self.start_btn.config(state='disabled', bg='#6c7086')
        self.progress.start(10)
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state='disabled')

        thread = threading.Thread(target=self.run_transcription, daemon=True)
        thread.start()

    def run_transcription(self):
        language = self.lang_var.get()
        with_timestamps = self.ts_var.get()
        completed = 0

        for file_path in self.files:
            try:
                content = transcribe_file(file_path, language, with_timestamps, self.log)
                if content:
                    out_path = save_transcript(file_path, content)
                    self.log(f'Saved: {os.path.basename(out_path)}\n')
                    completed += 1
            except Exception as e:
                self.log(f'Error ({os.path.basename(file_path)}): {e}\n')

        self.root.after(0, self.on_done, completed)

    def on_done(self, completed):
        self.progress.stop()
        self.running = False
        self.start_btn.config(state='normal', bg='#a6e3a1')
        self.log(f'Done! {completed}/{len(self.files)} file(s) transcribed.')
        messagebox.showinfo('Complete', f'Transcription complete!\n{completed} file(s) saved.')


def main():
    root = tk.Tk()
    app = TranscriberApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
