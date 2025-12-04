This folder points to the project's pytest-based tests located under tests/.

Run the test suite from the project root:

Windows (PowerShell):
.\.venv\Scripts\python.exe -m pytest -q

Unix/Bash:
.venv/bin/python -m pytest -q

The tests cover:
- Route existence and behavior
- Registration and login form validation
- Application configuration (SECRET_KEY from FLASK_SECRET)
