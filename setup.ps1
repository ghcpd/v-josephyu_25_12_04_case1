# PowerShell setup script
param()
python -m venv .venv
.\.venv\Scripts\Activate
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Virtual environment created and dependencies installed. Activate with: .\.venv\Scripts\Activate"