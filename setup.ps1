# PowerShell script to create the venv and install requirements
python -m venv .venv
# Activate (may require changing ExecutionPolicy)
. .\venv\Scripts\Activate.ps1 -ErrorAction SilentlyContinue
pip install --upgrade pip
pip install -r requirements.txt
