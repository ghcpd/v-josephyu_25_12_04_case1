#!/usr/bin/env bash
# Run pytest using the project's venv (Unix/WSL)
if [ -x ".venv/bin/python" ]; then
  .venv/bin/python -m pytest -q
elif [ -x ".venv/Scripts/python.exe" ]; then
  .venv/Scripts/python.exe -m pytest -q
else
  python -m pytest -q
fi
