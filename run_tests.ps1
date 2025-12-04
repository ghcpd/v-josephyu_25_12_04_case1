# Flask User Management Application Test Runner Script (Windows PowerShell)
# Runs all pytest tests with detailed output

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Flask User Management App - Test Suite" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if ($null -eq $env:VIRTUAL_ENV) {
    Write-Host "❌ Virtual environment not activated!" -ForegroundColor Red
    Write-Host "Please activate it first:" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    exit 1
}

Write-Host "Python: $(python --version)" -ForegroundColor Green
Write-Host "pytest: $(pytest --version)" -ForegroundColor Green
Write-Host ""

# Run all tests
Write-Host "Running tests..." -ForegroundColor Yellow
Write-Host ""

# Run with verbose output
if ($args.Length -gt 0) {
    python -m pytest tests/ -v `
        --tb=short `
        --color=yes `
        --durations=10 `
        @args
} else {
    python -m pytest tests/ -v `
        --tb=short `
        --color=yes `
        --durations=10
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test run complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
