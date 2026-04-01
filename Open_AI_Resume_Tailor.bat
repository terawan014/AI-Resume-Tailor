@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [Error] Python virtual environment not found.
    echo Please create it first with: python -m venv .venv
    pause
    exit /b 1
)

if not exist ".env" (
    echo [Error] .env file not found.
    echo Please create a .env file and add: GROQ_API_KEY=your_key_here
    pause
    exit /b 1
)

echo Starting AI Resume Tailor...
".venv\Scripts\python.exe" -m streamlit run app_ui.py --server.headless false
