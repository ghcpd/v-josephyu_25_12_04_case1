#!/bin/bash

# Flask User Management Application Setup Script (Linux/macOS/Bash)
# This script sets up the development environment

set -e  # Exit on error

echo "========================================"
echo "Flask User Management App - Setup"
echo "========================================"

# Check Python version
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "[2/5] Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "[3/5] Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "[4/5] Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"

# Install dependencies
echo ""
echo "[5/5] Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Initialize database
echo ""
echo "Initializing database..."
python3 -c "
from app import app
from models import init_db
with app.app_context():
    init_db(app)
print('✓ Database initialized')
"

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To start the development server, run:"
echo "  python app.py"
echo ""
echo "To run tests, run:"
echo "  pytest tests/"
echo ""
