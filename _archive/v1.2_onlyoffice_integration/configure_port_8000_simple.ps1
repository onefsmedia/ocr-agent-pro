# OnlyOffice Port Configuration Script for Port 8000
# Changes OnlyOffice Document Server from port 80 to port 8000

Write-Host "CONFIGURING ONLYOFFICE DOCUMENT SERVER TO PORT 8000" -ForegroundColor Yellow
Write-Host "======================================================"

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-NOT $isAdmin) {
    Write-Host "This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Right-click PowerShell -> 'Run as Administrator'" -ForegroundColor Cyan
    pause
    exit 1
}

$nginxConfPath = "C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\nginx.conf"

# Check if files exist
if (-not (Test-Path $nginxConfPath)) {
    Write-Host "nginx.conf not found at: $nginxConfPath" -ForegroundColor Red
    Write-Host "OnlyOffice Document Server may not be installed correctly." -ForegroundColor Yellow
    exit 1
}

Write-Host "Found OnlyOffice configuration files" -ForegroundColor Green

# Stop OnlyOffice services first
Write-Host "Stopping OnlyOffice services..." -ForegroundColor Yellow
$services = @("DsProxySvc", "DsDocServiceSvc", "DsConverterSvc")

foreach ($service in $services) {
    try {
        $svc = Get-Service -Name $service -ErrorAction SilentlyContinue
        if ($svc -and $svc.Status -eq "Running") {
            Stop-Service $service -Force
            Write-Host "  Stopped: $service" -ForegroundColor Green
        }
    } catch {
        Write-Host "  Could not stop: $service" -ForegroundColor Yellow
    }
}

# Backup original configuration
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupPath = "$nginxConfPath.backup.$timestamp"
Copy-Item $nginxConfPath $backupPath
Write-Host "Backup created: $backupPath" -ForegroundColor Cyan

# Read and modify nginx.conf
Write-Host "Updating nginx.conf for port 8000..." -ForegroundColor Yellow
$content = Get-Content $nginxConfPath

# Replace port 80 with 8000
$newContent = $content -replace "listen\s+80;", "listen 8000;"
$newContent = $newContent -replace "listen\s+\[::]:80;", "listen [::]:8000;"

# Write back the configuration
$newContent | Set-Content $nginxConfPath
Write-Host "  nginx.conf updated to use port 8000" -ForegroundColor Green

# Start services back up
Write-Host "Starting OnlyOffice services..." -ForegroundColor Yellow
foreach ($service in $services) {
    try {
        Start-Service $service
        Write-Host "  Started: $service" -ForegroundColor Green
    } catch {
        Write-Host "  Failed to start: $service" -ForegroundColor Red
    }
}

# Wait for services to start
Write-Host "Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Test the new port
Write-Host "Testing port 8000 configuration..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "  SUCCESS! OnlyOffice is accessible on port 8000" -ForegroundColor Green
        $success = $true
    }
} catch {
    Write-Host "  Port 8000 not yet accessible, may need more time" -ForegroundColor Yellow
    $success = $false
}

Write-Host ""
Write-Host "CONFIGURATION COMPLETE!" -ForegroundColor Green
Write-Host "  Port changed from 80 to 8000" -ForegroundColor White
Write-Host "  Document Server URL: http://localhost:8000" -ForegroundColor White
Write-Host "  Backup created: $backupPath" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Test OnlyOffice: http://localhost:8000" -ForegroundColor White
Write-Host "  2. Test OCR Agent connection in Settings Panel" -ForegroundColor White
Write-Host ""