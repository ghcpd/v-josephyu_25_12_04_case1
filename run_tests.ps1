"Run pytest in the .venv or system python if necessary"
if (Test-Path -Path .venv\Scripts\python.exe) {
    & .\\venv\\Scripts\\python.exe -m pytest -q
} else {
    python -m pytest -q
}
