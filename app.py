"""Aplikasi desktop Audio Transcriber — jalankan dengan python app.py."""
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

ROOT = Path(__file__).resolve().parent


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Transcriber | Satar")
        self.geometry("900x700")
        self.minsize(700, 580)
        self.process = None
        self.cancelled = False
        self.events = queue.Queue()
        self.audio = tk.StringVar()
        self.output = tk.StringVar(value=str(ROOT / "outputs"))
        self.model = tk.StringVar(value="medium")
        self.language = tk.StringVar(value="Indonesia")
        self.device = tk.StringVar(value="Otomatis")
        self.status = tk.StringVar(value="Siap. Pilih audio untuk memulai.")
        self.result_dir = None
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f3f7fb")
        style.configure("TLabel", background="#f3f7fb", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        frame = ttk.Frame(self, padding=24)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(10, weight=1)
        ttk.Label(frame, text="Audio Transcriber", font=("Segoe UI", 24, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        ttk.Label(frame, text="Ubah rekaman menjadi teks dan subtitle dengan Whisper.").grid(row=1, column=0, sticky="w", pady=(0, 20))
        self.controls = []
        for row, label, variable, action in [(2, "File audio / video", self.audio, self.pick_audio), (4, "Folder hasil", self.output, self.pick_output)]:
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w")
            line = ttk.Frame(frame)
            line.grid(row=row+1, column=0, sticky="ew", pady=(5, 12))
            line.columnconfigure(0, weight=1)
            entry = ttk.Entry(line, textvariable=variable)
            entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
            button = ttk.Button(line, text="Pilih...", command=action)
            button.grid(row=0, column=1)
            self.controls.extend([entry, button])
        options = ttk.Frame(frame)
        options.grid(row=6, column=0, sticky="ew")
        for column, (label, variable, values) in enumerate([
            ("Model", self.model, ["tiny", "base", "small", "medium", "turbo"]),
            ("Bahasa", self.language, ["Indonesia", "Inggris", "Deteksi otomatis"]),
            ("Perangkat", self.device, ["Otomatis", "CPU", "CUDA / GPU"]),
        ]):
            options.columnconfigure(column, weight=1)
            ttk.Label(options, text=label).grid(row=0, column=column, sticky="w")
            combo = ttk.Combobox(options, textvariable=variable, values=values, state="readonly", width=18)
            combo.grid(row=1, column=column, sticky="ew", padx=(0, 10), pady=5)
            self.controls.append(combo)
        ttk.Label(frame, text="Medium: pilihan awal untuk laptopmu. Jika memori GPU penuh, pilih small.").grid(row=7, column=0, sticky="w", pady=8)
        buttons = ttk.Frame(frame)
        buttons.grid(row=8, column=0, sticky="w", pady=8)
        self.start_button = ttk.Button(buttons, text="Transkripsikan", command=self.start)
        self.start_button.pack(side="left", padx=(0, 8))
        self.stop_button = ttk.Button(buttons, text="Hentikan", command=self.stop, state="disabled")
        self.stop_button.pack(side="left", padx=(0, 8))
        self.open_button = ttk.Button(buttons, text="Buka hasil", command=self.open_output, state="disabled")
        self.open_button.pack(side="left")
        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.grid(row=9, column=0, sticky="ew", pady=8)
        self.log = ScrolledText(frame, wrap="word", font=("Consolas", 10), height=12, state="disabled")
        self.log.grid(row=10, column=0, sticky="nsew")
        ttk.Label(frame, textvariable=self.status, wraplength=800).grid(row=11, column=0, sticky="w", pady=(10, 0))
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.after(100, self.poll)

    def pick_audio(self):
        value = filedialog.askopenfilename(filetypes=[("Audio / Video", "*.mp3 *.m4a *.wav *.mp4 *.flac *.ogg *.aac *.webm"), ("Semua file", "*.*")])
        if value:
            self.audio.set(value)

    def pick_output(self):
        value = filedialog.askdirectory()
        if value:
            self.output.set(value)

    def append(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    def start(self):
        audio = Path(self.audio.get())
        if not audio.is_file() or not self.output.get().strip():
            messagebox.showerror("Periksa input", "Pilih file audio dan folder hasil yang valid.")
            return
        # Folder unik: transkripsi sebelumnya tidak ditimpa.
        self.result_dir = Path(self.output.get()) / (audio.stem + "_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        command = [sys.executable, "-u", str(ROOT / "worker.py"), str(audio), "--output", str(self.result_dir), "--model", self.model.get(), "--language", {"Indonesia": "id", "Inggris": "en", "Deteksi otomatis": "auto"}[self.language.get()], "--device", {"Otomatis": "auto", "CPU": "cpu", "CUDA / GPU": "cuda"}[self.device.get()]]
        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", env=env, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        except OSError as error:
            messagebox.showerror("Tidak bisa memulai", str(error))
            return
        self.cancelled = False
        self.append("\n=== Transkripsi baru ===\n")
        for widget in self.controls:
            widget.configure(state="disabled")
        self.start_button.configure(state="disabled")
        self.open_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.progress.start()
        self.status.set("Sedang memproses. Unduhan model pertama membutuhkan internet.")
        threading.Thread(target=self.read_process, args=(self.process,), daemon=True).start()

    def read_process(self, process):
        for line in process.stdout:
            self.events.put(("log", line))
        process.stdout.close()
        self.events.put(("done", process.wait()))

    def poll(self):
        for _ in range(100):
            try:
                kind, value = self.events.get_nowait()
            except queue.Empty:
                break
            if kind == "log":
                self.append(value)
            else:
                self.progress.stop()
                self.process = None
                self.start_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                for widget in self.controls:
                    widget.configure(state="readonly" if isinstance(widget, ttk.Combobox) else "normal")
                success = value == 0 and not self.cancelled
                self.open_button.configure(state="normal" if success else "disabled")
                self.status.set(f"Selesai: {self.result_dir}" if success else "Dihentikan." if self.cancelled else "Gagal. Periksa log; jika GPU penuh, gunakan model small atau CPU.")
        self.after(100, self.poll)

    def stop(self):
        if self.process and self.process.poll() is None:
            self.cancelled = True
            # Hentikan seluruh pohon proses, termasuk konversi FFmpeg.
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(self.process.pid), "/T", "/F"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                self.process.terminate()

    def open_output(self):
        if self.result_dir and self.result_dir.is_dir():
            if os.name == "nt":
                os.startfile(str(self.result_dir))
            else:
                subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", str(self.result_dir)])

    def close(self):
        if self.process and self.process.poll() is None:
            if not messagebox.askyesno("Tutup aplikasi", "Transkripsi masih berjalan. Hentikan dan tutup?"):
                return
            self.stop()
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
