#!/usr/bin/env bash
set -euo pipefail
# Use the venv's python to run tests
.venv/bin/python -m pytest -q
