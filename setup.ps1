# Flask User Management Application Setup Script (Windows PowerShell)
# This script sets up the development environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Flask User Management App - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check Python version
Write-Host ""
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8 or later." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv .venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "[4/5] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "✓ pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[5/5] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Initialize database
Write-Host ""
Write-Host "Initializing database..." -ForegroundColor Yellow
python -c "
from app import app
from models import init_db
with app.app_context():
    init_db(app)
print('✓ Database initialized')
"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To activate the virtual environment, run:" -ForegroundColor White
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the development server, run:" -ForegroundColor White
Write-Host "  python app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run tests, run:" -ForegroundColor White
Write-Host "  pytest tests/" -ForegroundColor Cyan
Write-Host ""
