param([string]$Python = "$env:USERPROFILE\CNN-Praktikum\.venv\Scripts\python.exe")
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Python)) { throw 'Python tidak ditemukan. Tentukan parameter -Python.' }
& $Python -c "import torch, tkinter; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available())"
if ($LASTEXITCODE -ne 0) { throw 'Gunakan Python dengan PyTorch dan Tkinter. Lihat README.' }
& $Python -m pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Instalasi gagal.' }
& $Python -c "import whisper, imageio_ffmpeg, numpy; print('Dependensi siap')"
if ($LASTEXITCODE -ne 0) { throw 'Pemeriksaan gagal.' }
Write-Host 'Siap. Jalankan Run.ps1.' -ForegroundColor Green
