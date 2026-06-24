$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $root "backend"
$venvPython = Join-Path $root ".venv\Scripts\uvicorn.exe"

if (-not (Test-Path $venvPython)) {
  Write-Host "No se encontró el entorno virtual. Ejecuta primero:"
  Write-Host "  python -m venv .venv"
  Write-Host "  .\.venv\Scripts\pip install -r backend\requirements.txt"
  exit 1
}

Set-Location $backendDir
Write-Host "Iniciando backend en http://127.0.0.1:8000 ..."
& $venvPython app.main:app --reload --host 127.0.0.1 --port 8000
