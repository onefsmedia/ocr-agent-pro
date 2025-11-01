@echo off
title OCR Agent Pro - Waitress Server
color 0A

echo ============================================
echo   OCR Agent Pro - Production Server
echo ============================================
echo.

REM Check if we're in the correct directory
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Please run this script from the OCR Agent directory
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH!
    echo Please install Python or add it to your PATH
    pause
    exit /b 1
)

echo Checking dependencies...
python -c "import waitress; print('Waitress: OK')" 2>nul
if errorlevel 1 (
    echo Installing Waitress server...
    python -m pip install waitress
)

python -c "from app import create_app; print('Flask app: OK')" 2>nul
if errorlevel 1 (
    echo ERROR: Flask application not working!
    echo Please check your installation
    pause
    exit /b 1
)

echo.
echo Starting OCR Agent Pro with Waitress server...
echo Server will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

REM Start the server
python app.py

echo.
echo Server stopped.
pause