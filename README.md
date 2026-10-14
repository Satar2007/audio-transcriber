# Audio Transcriber

Aplikasi desktop Python dengan tampilan Indonesia untuk transkripsi lokal menggunakan OpenAI Whisper. Dibuat untuk Rafael Paskah Bintang Pinasthi (Satar2007).

## Fitur

- Input MP3, M4A, WAV, MP4, FLAC, OGG, AAC, WEBM.
- Model tiny, base, small, medium, turbo; bahasa Indonesia, Inggris, atau otomatis.
- CPU atau CUDA/GPU NVIDIA; pemilihan perangkat otomatis.
- Hasil TXT, TXT dengan waktu, SRT, dan JSON dalam folder baru setiap pekerjaan.
- Log teks per segmen, tombol hentikan, dan buka folder hasil.
- FFmpeg dari imageio-ffmpeg: tidak perlu mengatur PATH.

## Laptop Paskah: Windows / PowerShell

Ekstrak proyek ke `C:\Users\b7235\Projects\audio-transcriber`, lalu:

```powershell
Set-Location 'C:\Users\b7235\Projects\audio-transcriber'
powershell -NoProfile -ExecutionPolicy Bypass -File .\Install.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\Run.ps1
```

Skrip memakai Python yang sudah ada di `C:\Users\b7235\CNN-Praktikum\.venv\Scripts\python.exe`. Instalasi menambah dependensi ke environment ini, tanpa perintah upgrade PyTorch. Parameter `-Python` dapat digunakan untuk interpreter lain.

Alternatif tanpa skrip:

```powershell
$python = "$env:USERPROFILE\CNN-Praktikum\.venv\Scripts\python.exe"
& $python -m pip install -r .\requirements.txt
& $python .\app.py
```

VS Code: buka folder proyek, pilih **Python: Select Interpreter**, pilih Python di atas, lalu jalankan `app.py`.

## Pemakaian

1. Pilih file audio dan folder hasil.
2. Mulai dengan medium / Indonesia / Otomatis.
3. Klik Transkripsikan, tunggu selesai, lalu Buka hasil.

Indikator bergerak menunjukkan proses berjalan, bukan persentase. Log menampilkan tahap dan teks per segmen. Hentikan membatalkan pekerjaan; tidak ada resume. Hasil: `transkrip.txt`, `transkrip_waktu.txt`, `subtitle.srt`, `hasil.json`.

## Komputer lain

Gunakan Python yang kompatibel dengan PyTorch dan Whisper; Python 3.11 atau 3.12 dapat menjadi titik awal. Buat environment lalu pasang PyTorch sesuai perangkat melalui https://pytorch.org/get-started/locally/.

```powershell
py -3.11 -m venv .venv
$python = '.\.venv\Scripts\python.exe'
# Pasang PyTorch menggunakan perintah dari situs resmi, lalu:
& $python -m pip install -r .\requirements.txt
& $python .\app.py
```

Tkinter biasanya disertakan installer Python Windows; Linux mungkin membutuhkan `python3-tk`. GPU aplikasi memakai CUDA, perangkat lain memakai CPU.

## Mode terminal

```powershell
& $python .\worker.py 'C:\lokasi\rekaman.mp3' --output '.\outputs\rekaman-01' --model medium --language id --device auto
```

Gunakan output baru setiap menjalankan CLI; CLI menimpa empat berkas jika folder sama dipakai.

## GitHub

Buat repo kosong `audio-transcriber` di akun GitHub tanpa README otomatis. Dari folder proyek:

```powershell
git init
git add .
git status
# Periksa daftar berkas: jangan sertakan audio atau hasil pribadi.
git commit -m "Build desktop audio transcriber"
git branch -M main
git remote add origin https://github.com/Satar2007/audio-transcriber.git
git push -u origin main
```

Repo menyimpan kode; transkripsi berjalan di laptop pengguna. `.gitignore` mengecualikan audio, model, environment, dan folder hasil default. Tambahkan folder output lain di dalam repo ke `.gitignore` sebelum commit.

## Privasi dan batasan

Tidak memakai API key; audio diproses lokal. Instalasi dan unduhan model pertama membutuhkan internet. Setelah model tersedia, transkripsi bisa offline. Hasil perlu ditinjau terutama nama, angka, suara pelan, bagian hening, dan pembicara bertumpuk. Tidak ada identifikasi pembicara. Seluruh audio dimuat ke RAM.

Jika memori CUDA penuh, pilih small atau CPU. Hindari training GPU bersamaan. Download model gagal: periksa koneksi lalu ulangi. File rusak/tanpa trek audio: lihat log FFmpeg.

## Pemeriksaan

```powershell
& $python -m unittest discover -s tests -v
& $python -m compileall -q app.py worker.py exporter.py
```

Tes memeriksa format waktu dan ekspor Unicode/SRT. Transkripsi asli harus diuji pada komputer dengan dependensi dan model terpasang.

## Referensi dan lisensi

- https://github.com/openai/whisper
- https://pytorch.org/get-started/locally/
- https://github.com/imageio/imageio-ffmpeg

Dependensi mengikuti lisensi masing-masing. Lisensi distribusi kode proyek belum ditetapkan.
