@echo off
echo ===================================================
echo Starting InternMatch AI Backend (FastAPI on Port 8000)
echo ===================================================
call .venv\Scripts\activate.bat
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
pause
