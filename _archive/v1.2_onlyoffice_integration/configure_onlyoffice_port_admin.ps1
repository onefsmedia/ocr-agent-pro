# Run this script as Administrator to configure OnlyOffice port
# Script: configure_onlyoffice_port_admin.ps1

if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "CONFIGURING ONLYOFFICE DOCUMENT SERVER PORT (Admin Mode)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

$nginxConfPath = "C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\nginx.conf"
$dsConfPath = "C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\ds.conf"

# Check current configuration
Write-Host "Current nginx.conf:" -ForegroundColor Yellow
if (Test-Path $nginxConfPath) {
    Get-Content $nginxConfPath | Where-Object { $_ -match "listen" } | ForEach-Object { Write-Host "  $_" -ForegroundColor Cyan }
} else {
    Write-Host "nginx.conf not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Current ds.conf:" -ForegroundColor Yellow
if (Test-Path $dsConfPath) {
    Get-Content $dsConfPath | Where-Object { $_ -match "listen" } | ForEach-Object { Write-Host "  $_" -ForegroundColor Cyan }
}

# Stop services
Write-Host "Stopping OnlyOffice services..." -ForegroundColor Yellow
$services = @(
    "ONLYOFFICE Document Server Proxy",
    "ONLYOFFICE Document Server DocService", 
    "ONLYOFFICE Document Server Converter"
)

foreach ($service in $services) {
    try {
        Stop-Service $service -Force -ErrorAction SilentlyContinue
        Write-Host "  Stopped: $service" -ForegroundColor Green
    } catch {
        Write-Host "  Could not stop: $service" -ForegroundColor Yellow
    }
}

# Backup and modify nginx.conf
Write-Host "Modifying nginx.conf..." -ForegroundColor Yellow
$backupPath = "$nginxConfPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
try {
    Copy-Item $nginxConfPath $backupPath
    Write-Host "  Backup created: $backupPath" -ForegroundColor Green
    
    $content = Get-Content $nginxConfPath
    $newContent = $content -replace "listen\s+80;", "listen 8096;"
    $newContent = $newContent -replace "listen\s+\[::]:80;", "listen [::]:8096;"
    $newContent | Set-Content $nginxConfPath
    
    Write-Host "  nginx.conf updated to use port 8096" -ForegroundColor Green
} catch {
    Write-Host "  Error modifying nginx.conf: $($_.Exception.Message)" -ForegroundColor Red
}

# Backup and modify ds.conf
if (Test-Path $dsConfPath) {
    Write-Host "Modifying ds.conf..." -ForegroundColor Yellow
    $backupDsPath = "$dsConfPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    try {
        Copy-Item $dsConfPath $backupDsPath
        Write-Host "  Backup created: $backupDsPath" -ForegroundColor Green
        
        $dsContent = Get-Content $dsConfPath
        $newDsContent = $dsContent -replace "listen\s+80;", "listen 8096;"
        $newDsContent = $newDsContent -replace "listen\s+\[::]:80;", "listen [::]:8096;"
        $newDsContent | Set-Content $dsConfPath
        
        Write-Host "  ds.conf updated to use port 8096" -ForegroundColor Green
    } catch {
        Write-Host "  Error modifying ds.conf: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Start services
Write-Host "Starting OnlyOffice services..." -ForegroundColor Yellow
foreach ($service in $services) {
    try {
        Start-Service $service -ErrorAction SilentlyContinue
        Write-Host "  Started: $service" -ForegroundColor Green
    } catch {
        Write-Host "  Could not start: $service" -ForegroundColor Yellow
    }
}

# Wait and test
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "Testing new port configuration..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8096/welcome" -UseBasicParsing -TimeoutSec 15 -ErrorAction SilentlyContinue
    Write-Host "SUCCESS! OnlyOffice Document Server is now accessible on port 8096!" -ForegroundColor Green
    Write-Host "Response Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Port 8096 not yet accessible. Trying healthcheck endpoint..." -ForegroundColor Yellow
    try {
        $health = Invoke-WebRequest -Uri "http://localhost:8096/healthcheck" -UseBasicParsing -TimeoutSec 15 -ErrorAction SilentlyContinue
        Write-Host "Healthcheck accessible on port 8096! Status: $($health.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "Services may need more time to start. Check manually at: http://localhost:8096" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "CONFIGURATION COMPLETE!" -ForegroundColor Green
Write-Host "New OnlyOffice URL: http://localhost:8096" -ForegroundColor White
Write-Host ""

# Show current service status
Write-Host "Current service status:" -ForegroundColor Yellow
Get-Service | Where-Object { $_.Name -like "*onlyoffice*" -or $_.DisplayName -like "*ONLYOFFICE*" } | 
    Select-Object DisplayName, Status | Format-Table -AutoSize

pause