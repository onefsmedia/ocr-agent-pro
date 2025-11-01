@echo off
title OCR Agent Pro Server
cd /d "c:\OCR Agent"

echo.
echo ========================================
echo    OCR Agent Pro Server Launcher
echo ========================================
echo.

REM Kill any existing Python processes on port 5000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    echo Stopping existing process on port 5000...
    taskkill /PID %%a /F >nul 2>&1
)

echo Starting Flask server...
echo Server will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start server with process isolation
start /wait /B python ultra_simple_server.py

echo.
echo Server stopped.
pause