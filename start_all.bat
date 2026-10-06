@echo off
echo ===================================================
echo Launching InternMatch AI Full Stack (Backend + Frontend)
echo ===================================================
start "InternMatch AI Backend (FastAPI)" cmd /c "start_backend.bat"
start "InternMatch AI Frontend (Next.js)" cmd /c "start_frontend.bat"
echo Services are starting:
echo  - Backend API: http://127.0.0.1:8000/docs
echo  - Frontend Web UI: http://localhost:3000
echo.
