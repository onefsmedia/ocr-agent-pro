@echo off
echo Fixing Docker Desktop Permissions...
echo.

echo Stopping Docker processes...
taskkill /f /im "Docker Desktop.exe" 2>nul
taskkill /f /im "dockerd.exe" 2>nul

echo.
echo Fixing named pipe permissions...
icacls "\\.\pipe\docker_engine" /grant Everyone:F 2>nul
icacls "\\.\pipe\dockerDesktopLinuxEngine" /grant Everyone:F 2>nul

echo.
echo Restarting Docker service...
net stop com.docker.service 2>nul
net start com.docker.service

echo.
echo Starting Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"

echo.
echo Waiting for Docker to start...
timeout /t 20 /nobreak > nul

echo.
echo Testing Docker...
docker version

echo.
echo Docker should now be working!
pause