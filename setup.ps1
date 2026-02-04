param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (-Not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment (.venv) with $Python" -ForegroundColor Cyan
    & $Python -m venv .venv
} else {
    Write-Host ".venv already exists" -ForegroundColor Yellow
}

$venvPython = Join-Path $root ".venv\Scripts\python.exe"
if (-Not (Test-Path $venvPython)) {
    throw ".venv python not found at $venvPython"
}

& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host "Virtual environment ready." -ForegroundColor Green
