<div align="center">

# 🎙️ Audio Transcriber

**Dari rekaman menjadi teks dan subtitle.**

Aplikasi desktop Python dengan antarmuka bahasa Indonesia, ditenagai OpenAI Whisper.

[![Python checks](https://github.com/Satar2007/audio-transcriber/actions/workflows/check.yml/badge.svg)](https://github.com/Satar2007/audio-transcriber/actions/workflows/check.yml)
![Python](https://img.shields.io/badge/Python-Desktop_App-3776AB?logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/Engine-OpenAI_Whisper-412991)
![Processing](https://img.shields.io/badge/Processing-Local-15803D)

[Mulai menggunakan](#-mulai-menggunakan) · [Cara penggunaan](#-cara-penggunaan) · [Troubleshooting](#-troubleshooting)

</div>

---

Audio Transcriber membantu mengubah rekaman kuliah, diskusi, wawancara, dan audio dari video menjadi transkrip yang mudah dibaca. Pilih file, tentukan model dan bahasa, lalu simpan hasil sebagai teks atau subtitle.

Audio diproses di komputer pengguna. **Tidak memerlukan API key atau layanan transkripsi berbayar.** Instalasi dependensi dan unduhan model pertama memerlukan internet.

## ✨ Fitur

| Fitur | Dukungan |
| --- | --- |
| Input audio dan video | MP3, M4A, WAV, MP4, FLAC, OGG, AAC, WEBM yang dapat dibaca FFmpeg |
| Model Whisper | `tiny`, `base`, `small`, `medium`, `turbo` |
| Bahasa | Indonesia, Inggris, atau deteksi otomatis |
| Perangkat | Otomatis, CPU, atau GPU NVIDIA melalui CUDA |
| Ekspor | TXT, TXT dengan waktu, SRT, dan JSON |
| Pemantauan | Log tahap proses dan teks per segmen |
| Kontrol | Hentikan transkripsi dan buka folder hasil |
| Penyimpanan | Folder baru untuk setiap transkripsi dari aplikasi desktop |

Konversi audio menggunakan FFmpeg yang disediakan melalui `imageio-ffmpeg`, sehingga tidak perlu menambahkan FFmpeg ke PATH secara manual.

## 🚀 Mulai menggunakan

### 1. Unduh proyek

```powershell
git clone https://github.com/Satar2007/audio-transcriber.git
Set-Location .\audio-transcriber
```

Atau pilih **Code → Download ZIP** di GitHub, ekstrak, lalu buka folder yang berisi `app.py`.

### 2. Siapkan Python

Gunakan Python dengan **Tkinter** dan versi PyTorch yang kompatibel. Python 3.11 atau 3.12 dapat menjadi titik awal untuk environment baru.

```powershell
py -3.11 -m venv .venv
$python = '.\.venv\Scripts\python.exe'
```

Jika sudah mempunyai environment Python dengan PyTorch, gunakan interpreter tersebut:

```powershell
$python = 'C:\lokasi\environment\Scripts\python.exe'
```

### 3. Pasang PyTorch dan dependensi

Untuk penggunaan CPU:

```powershell
& $python -m pip install torch
& $python -m pip install -r .\requirements.txt
```

Untuk GPU NVIDIA, gunakan perintah instalasi dari [pemilih resmi PyTorch](https://pytorch.org/get-started/locally/) sesuai sistem dan dukungan CUDA. Jika PyTorch sudah terpasang, cukup pasang `requirements.txt`.

Periksa ketersediaan GPU:

```powershell
& $python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

### 4. Buka aplikasi

```powershell
& $python .\app.py
```

Di **VS Code**, buka folder proyek dan pilih interpreter yang sama melalui **Python: Select Interpreter**, lalu jalankan `app.py`.

<details>
<summary><strong>Alternatif: skrip PowerShell</strong></summary>

Skrip dapat menerima lokasi Python yang kamu gunakan:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Install.ps1 -Python $python
powershell -NoProfile -ExecutionPolicy Bypass -File .\Run.ps1 -Python $python
```

`Install.ps1` memeriksa PyTorch dan Tkinter, kemudian memasang dependensi aplikasi. Skrip ini tidak memasang PyTorch secara terpisah.

Tanpa parameter `-Python`, skrip memakai environment pengembang di `$env:USERPROFILE\CNN-Praktikum\.venv\Scripts\python.exe`.

</details>

## 🖥️ Cara penggunaan

1. Klik **Pilih…** pada bagian **File audio / video**.
2. Tentukan **Folder hasil**.
3. Pilih model, bahasa, dan perangkat.
4. Klik **Transkripsikan**.
5. Tunggu status **Selesai**, kemudian klik **Buka hasil**.

Untuk memulai, gunakan bahasa **Indonesia** dan perangkat **Otomatis**. Model `medium` bisa dipakai jika memori perangkat mencukupi; pilih `small` bila GPU kehabisan memori.

Indikator bergerak menunjukkan proses masih berjalan, **bukan persentase penyelesaian**. Log menampilkan teks per segmen selama transkripsi. Tombol **Hentikan** membatalkan pekerjaan; belum ada fitur melanjutkan proses yang dibatalkan.

## 📄 Hasil transkripsi

Setiap pekerjaan dari aplikasi desktop membuat folder dengan nama audio dan waktu proses:

```text
outputs/
└── rekaman_YYYYMMDD_HHMMSS_microseconds/
    ├── transkrip.txt
    ├── transkrip_waktu.txt
    ├── subtitle.srt
    └── hasil.json
```

| File | Isi |
| --- | --- |
| `transkrip.txt` | Teks lengkap tanpa penanda waktu |
| `transkrip_waktu.txt` | Teks per segmen dengan waktu mulai dan akhir |
| `subtitle.srt` | Subtitle dengan format waktu SRT |
| `hasil.json` | Hasil Whisper untuk pengolahan lanjutan |

Contoh format subtitle:

```srt
1
00:00:00,000 --> 00:00:03,250
Selamat pagi, hari ini kita membahas materi perkuliahan.
```

*Contoh di atas merupakan ilustrasi format.*

## ⌨️ Mode terminal

Untuk menjalankan transkripsi tanpa membuka antarmuka:

```powershell
& $python .\worker.py 'C:\Audio\rekaman.mp3' `
    --output '.\outputs\rekaman-01' `
    --model medium `
    --language id `
    --device auto
```

| Parameter | Pilihan |
| --- | --- |
| `--output` | Folder hasil; wajib diberikan |
| `--model` | `tiny`, `base`, `small`, `medium`, `turbo` |
| `--language` | `id`, `en`, `auto` |
| `--device` | `auto`, `cpu`, `cuda` |

**Gunakan folder output baru untuk setiap pekerjaan CLI.** Berbeda dari aplikasi desktop, mode terminal menimpa empat file hasil jika folder yang sama digunakan kembali.

## 🧩 Cara kerja

1. FFmpeg mengambil trek audio dan mengonversinya menjadi WAV mono 16 kHz.
2. Whisper memuat model pada CPU atau GPU yang dipilih.
3. Rekaman ditranskripsikan dan teks segmen ditampilkan dalam log.
4. Hasil diekspor ke empat format.

Mesin transkripsi berjalan dalam proses terpisah agar jendela aplikasi tetap responsif. WAV sementara ditempatkan di direktori temporer saat konversi.

## 🔧 Troubleshooting

| Kendala | Langkah yang dapat dicoba |
| --- | --- |
| `CUDA: False` | Gunakan CPU atau periksa instalasi PyTorch dengan dukungan CUDA dan driver NVIDIA |
| `CUDA out of memory` | Pilih model lebih kecil seperti `small`, tutup aplikasi GPU lain, atau pilih CPU |
| Model gagal diunduh | Periksa koneksi internet lalu jalankan ulang |
| File tidak bisa dikonversi | Pastikan file tidak rusak dan memiliki trek audio; lihat pesan FFmpeg dalam log |
| `No module named ...` | Pasang dependensi memakai interpreter yang sama dengan aplikasi |
| Tkinter tidak tersedia | Gunakan instalasi Python dengan Tcl/Tk; Linux mungkin memerlukan paket `python3-tk` |
| `Install.ps1` tidak ditemukan | Masuk ke folder yang langsung berisi `Install.ps1` dan `app.py`; ZIP bisa menghasilkan folder berlapis |

Windows menjadi lingkungan penggunaan utama proyek ini. Kode juga menyediakan pembukaan folder hasil untuk macOS dan Linux, tetapi kedua platform tersebut belum diverifikasi dalam pengujian proyek.

## 🔒 Privasi dan batasan

- Aplikasi memproses audio secara lokal, tanpa mengunggahnya ke layanan transkripsi.
- Setelah dependensi dan model tersedia, transkripsi dapat dilakukan offline.
- Hasil perlu diperiksa, terutama nama orang, angka, istilah teknis, suara pelan, dan pembicara yang berbicara bersamaan.
- Aplikasi belum menyediakan pemisahan identitas pembicara atau editor transkrip.
- Seluruh audio dimuat ke RAM; kebutuhan memori meningkat untuk rekaman panjang.
- Waktu proses bergantung pada durasi audio, model, dan perangkat.

`.gitignore` mengecualikan audio, model, virtual environment, dan folder hasil default `outputs/`. Jika memilih folder hasil lain **di dalam repo**, tambahkan folder itu ke `.gitignore` sebelum melakukan commit.

## 🧪 Pemeriksaan kode

```powershell
& $python -m unittest discover -s tests -v
& $python -m compileall -q app.py worker.py exporter.py
```

Tes mencakup format waktu, pergantian menit pada timestamp, dan ekspor Unicode/SRT. GitHub Actions menjalankan tes tersebut dan pemeriksaan sintaks pada push atau pull request. Pengujian ini tidak menjalankan model Whisper atau memvalidasi akurasi transkripsi.

## 🛠️ Teknologi

- **Python + Tkinter** — aplikasi desktop.
- **OpenAI Whisper + PyTorch** — mesin transkripsi dan pemrosesan CPU/CUDA.
- **imageio-ffmpeg + NumPy** — konversi dan pembacaan audio.
- **GitHub Actions** — pemeriksaan kode otomatis.

## 👤 Pengembang

**Rafael Paskah Bintang Pinasthi** · [@Satar2007](https://github.com/Satar2007)

Masukan dan laporan masalah dapat disampaikan melalui [GitHub Issues](https://github.com/Satar2007/audio-transcriber/issues). Sertakan pesan error dan langkah reproduksi; hindari menyertakan rekaman pribadi.

## 📚 Referensi dan lisensi

- [OpenAI Whisper](https://github.com/openai/whisper)
- [PyTorch](https://pytorch.org/get-started/locally/)
- [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg)

Dependensi mengikuti lisensi masing-masing. Lisensi distribusi kode proyek ini belum ditetapkan.
