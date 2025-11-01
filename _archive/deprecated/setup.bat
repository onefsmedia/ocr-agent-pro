@echo off
REM OCR Agent Pro - Easy Setup and Management Script
echo.
echo ====================================
echo   OCR Agent Pro - Setup Manager
echo ====================================
echo.

:MENU
echo [1] Install Dependencies
echo [2] Test Direct Server
echo [3] Install Windows Service
echo [4] Start Service
echo [5] Stop Service  
echo [6] Service Status
echo [7] Uninstall Service
echo [8] View Logs
echo [9] Complete Setup (Dependencies + Service)
echo [0] Exit
echo.
set /p choice="Select option (0-9): "

if "%choice%"=="1" goto INSTALL_DEPS
if "%choice%"=="2" goto TEST_SERVER
if "%choice%"=="3" goto INSTALL_SERVICE
if "%choice%"=="4" goto START_SERVICE
if "%choice%"=="5" goto STOP_SERVICE
if "%choice%"=="6" goto SERVICE_STATUS
if "%choice%"=="7" goto UNINSTALL_SERVICE
if "%choice%"=="8" goto VIEW_LOGS
if "%choice%"=="9" goto COMPLETE_SETUP
if "%choice%"=="0" goto EXIT
goto MENU

:INSTALL_DEPS
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pywin32
echo.
echo ✅ Dependencies installed!
pause
goto MENU

:TEST_SERVER
echo.
echo Testing OCR Agent server (Ctrl+C to stop)...
python persistent_server.py
pause
goto MENU

:INSTALL_SERVICE
echo.
echo Installing Windows Service...
python windows_service.py install
echo.
echo ✅ Service installed! It will auto-start on boot.
pause
goto MENU

:START_SERVICE
echo.
echo Starting OCR Agent Pro service...
python windows_service.py start
echo.
echo 🌐 Access at: http://localhost:5000
pause
goto MENU

:STOP_SERVICE
echo.
echo Stopping OCR Agent Pro service...
python windows_service.py stop
pause
goto MENU

:SERVICE_STATUS
echo.
echo Checking service status...
python windows_service.py status
pause
goto MENU

:UNINSTALL_SERVICE
echo.
echo Uninstalling Windows Service...
python windows_service.py uninstall
pause
goto MENU

:VIEW_LOGS
echo.
echo Viewing recent logs...
if exist "logs\service.log" (
    powershell -Command "Get-Content 'logs\service.log' -Tail 20"
) else (
    echo No service logs found.
)
if exist "logs\server.log" (
    echo.
    echo Server logs:
    powershell -Command "Get-Content 'logs\server.log' -Tail 20"
) else (
    echo No server logs found.
)
pause
goto MENU

:COMPLETE_SETUP
echo.
echo ================================================
echo   Complete OCR Agent Pro Setup
echo ================================================
echo.
echo Step 1: Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pywin32
echo.
echo Step 2: Installing Windows service...
python windows_service.py install
echo.
echo Step 3: Starting service...
python windows_service.py start
echo.
echo ================================================
echo   🎉 Setup Complete!
echo ================================================
echo.
echo ✅ OCR Agent Pro is now running as a Windows service
echo ✅ Service will auto-start on system boot
echo ✅ Access your application at: http://localhost:5000
echo.
echo Service Management:
echo   • View logs: Option 8 from main menu
echo   • Stop service: Option 5 from main menu  
echo   • Check status: Option 6 from main menu
echo.
pause
goto MENU

:EXIT
echo.
echo Goodbye! 👋
exit /b 0