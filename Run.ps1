param([string]$Python = "$env:USERPROFILE\CNN-Praktikum\.venv\Scripts\python.exe")
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Python)) { throw 'Python tidak ditemukan. Tentukan parameter -Python.' }
& $Python (Join-Path $PSScriptRoot 'app.py')
if ($LASTEXITCODE -ne 0) { throw 'Aplikasi gagal. Periksa pesan error.' }
