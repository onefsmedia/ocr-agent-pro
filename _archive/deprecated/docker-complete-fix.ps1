# Docker Desktop Complete Fix Script
# This script completely resets Docker Desktop and fixes permission issues

Write-Host "=== Docker Desktop Complete Reset & Fix ===" -ForegroundColor Green
Write-Host ""

# Step 1: Completely stop all Docker processes
Write-Host "Step 1: Stopping all Docker processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*docker*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Stop-Service com.docker.service -Force -ErrorAction SilentlyContinue

# Step 2: Remove Docker Desktop data
Write-Host "Step 2: Cleaning Docker Desktop data..." -ForegroundColor Yellow
$dockerData = "$env:APPDATA\Docker"
$dockerDesktopData = "$env:APPDATA\Docker Desktop"
if (Test-Path $dockerData) { Remove-Item $dockerData -Recurse -Force -ErrorAction SilentlyContinue }
if (Test-Path $dockerDesktopData) { Remove-Item $dockerDesktopData -Recurse -Force -ErrorAction SilentlyContinue }

# Step 3: Fix named pipe permissions
Write-Host "Step 3: Fixing named pipe permissions..." -ForegroundColor Yellow
$pipes = @(
    "\\.\pipe\docker_engine",
    "\\.\pipe\dockerDesktopLinuxEngine",
    "\\.\pipe\docker_wsl"
)

foreach ($pipe in $pipes) {
    icacls $pipe /grant "Everyone:(F)" /T 2>$null
    icacls $pipe /grant "Users:(F)" /T 2>$null
    icacls $pipe /grant "$env:USERNAME:(F)" /T 2>$null
}

# Step 4: Enable required Windows features
Write-Host "Step 4: Enabling Windows features..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -All -NoRestart -ErrorAction SilentlyContinue
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -All -NoRestart -ErrorAction SilentlyContinue
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -All -NoRestart -ErrorAction SilentlyContinue

# Step 5: Update WSL2
Write-Host "Step 5: Updating WSL2..." -ForegroundColor Yellow
wsl --update
wsl --set-default-version 2

# Step 6: Registry fixes
Write-Host "Step 6: Applying registry fixes..." -ForegroundColor Yellow
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\com.docker.service"
if (Test-Path $regPath) {
    Set-ItemProperty -Path $regPath -Name "Start" -Value 2 -ErrorAction SilentlyContinue
}

# Step 7: Restart Docker service
Write-Host "Step 7: Starting Docker service..." -ForegroundColor Yellow
Start-Service com.docker.service -ErrorAction SilentlyContinue

# Step 8: Start Docker Desktop
Write-Host "Step 8: Starting Docker Desktop..." -ForegroundColor Yellow
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Docker Desktop reset complete!" -ForegroundColor Green
Write-Host "Please wait 2-3 minutes for Docker Desktop to fully start." -ForegroundColor Cyan
Write-Host ""

# Test commands
Write-Host "After Docker starts, test with these commands:" -ForegroundColor Yellow
Write-Host "docker --version" -ForegroundColor White
Write-Host "docker info" -ForegroundColor White
Write-Host ""
Write-Host "If issues persist, try running Docker Desktop as Administrator." -ForegroundColor Cyan