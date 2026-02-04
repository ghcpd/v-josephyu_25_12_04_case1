#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PYTHON=${PYTHON:-python3}

if [ ! -d .venv ]; then
  echo "Creating virtual environment (.venv) with $PYTHON"
  "$PYTHON" -m venv .venv
else
  echo ".venv already exists"
fi

# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment ready."
