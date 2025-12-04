#!/bin/bash

# Flask User Management Application Test Runner Script (Linux/macOS/Bash)
# Runs all pytest tests with detailed output

set -e  # Exit on error

echo "========================================"
echo "Flask User Management App - Test Suite"
echo "========================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Virtual environment not activated!"
    echo "Please activate it first:"
    echo "  source .venv/bin/activate"
    exit 1
fi

echo "Python: $(python --version)"
echo "pytest: $(pytest --version)"
echo ""

# Run all tests
echo "Running tests..."
echo ""

# Run with verbose output and show test coverage
if command -v pytest &> /dev/null; then
    pytest tests/ -v \
        --tb=short \
        --color=yes \
        --durations=10 \
        "$@"
else
    python -m pytest tests/ -v \
        --tb=short \
        --color=yes \
        --durations=10 \
        "$@"
fi

echo ""
echo "========================================"
echo "Test run complete!"
echo "========================================"
