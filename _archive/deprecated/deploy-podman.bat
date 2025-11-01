@echo off
echo 🐘 OCR Agent - Podman Desktop Deployment
echo =========================================
echo.

REM Check if Podman is installed
podman --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Podman is not installed or not in PATH
    echo Please install Podman Desktop from: https://podman-desktop.io/
    pause
    exit /b 1
)

echo ✅ Podman found
echo.

REM Check if docker-compose.yml exists
if not exist "docker-compose.yml" (
    echo ❌ docker-compose.yml not found in current directory
    echo Please run this script from the OCR Agent root directory
    pause
    exit /b 1
)

echo ✅ docker-compose.yml found
echo.

echo 🚀 Starting OCR Agent deployment...
echo.

REM Stop any existing containers
echo 🛑 Stopping existing containers...
podman-compose down 2>nul

echo.
echo 🔨 Building and starting services...
podman-compose up -d --build

if %errorlevel% neq 0 (
    echo.
    echo ❌ Deployment failed! Check the logs above for errors.
    echo.
    echo Common solutions:
    echo - Make sure Podman Desktop is running
    echo - Check if ports 5000, 5432, 6379 are available
    echo - Verify docker-compose.yml syntax
    echo.
    pause
    exit /b 1
)

echo.
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo 📊 Checking service status...
podman-compose ps

echo.
echo ✅ OCR Agent deployed successfully!
echo.
echo 🌐 Access your application at:
echo    ➤ Web Interface: http://localhost:5000
echo    ➤ PostgreSQL: localhost:5432 (user: renderman, password: Master@2025)
echo    ➤ Redis: localhost:6379
echo.
echo 📝 Useful commands:
echo    ➤ View logs: podman-compose logs -f ocr_agent
echo    ➤ Check status: podman-compose ps
echo    ➤ Stop services: podman-compose down
echo    ➤ Update app: podman-compose up -d --build
echo.
echo 📚 For detailed documentation, see DEPLOYMENT.md
echo.

REM Try to open the web browser
echo 🌍 Opening web browser...
start http://localhost:5000

echo.
echo Press any key to exit...
pause >nul