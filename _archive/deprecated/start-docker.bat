@echo off
echo Starting OCR Agent with Docker...
echo.

echo Checking Docker status...
docker --version
if %errorlevel% neq 0 (
    echo Docker is not running or not installed!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo.
echo Stopping any existing containers...
docker-compose down

echo.
echo Building and starting OCR Agent containers...
docker-compose up --build -d

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak > nul

echo.
echo Checking container status...
docker-compose ps

echo.
echo OCR Agent is starting up...
echo.
echo Web Application: http://localhost:5000
echo PostgreSQL: localhost:5432 (ocr_user/ocr_password)
echo OnlyOffice: http://localhost:8000
echo Ollama LLM: http://localhost:11434
echo.

echo Showing logs (Ctrl+C to exit log view)...
docker-compose logs -f web