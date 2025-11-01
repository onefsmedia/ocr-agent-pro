@echo off
title OCR Agent Pro - Production Server
cd /d "c:\OCR Agent"

echo.
echo ===================================================
echo    OCR Agent Pro - Starting in New Window
echo ===================================================
echo.

REM Clean up any existing processes on port 5000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo Cleaning up port 5000...
    taskkill /PID %%a /F >nul 2>&1
)

echo Starting OCR Agent Pro in separate window...
echo This window will close, but the server will continue running.
echo.

REM Start server in new window that stays open
start "OCR Agent Pro Server" cmd /k "python production_server.py"

echo.
echo ✅ Server started in new window!
echo ✅ Access at: http://localhost:5000
echo.
pause