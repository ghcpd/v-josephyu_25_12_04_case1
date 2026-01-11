#!/usr/bin/env bash
# Create venv and install requirements (Linux / macOS / WSL)
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
