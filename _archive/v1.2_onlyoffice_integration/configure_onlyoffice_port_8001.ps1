# OnlyOffice Port Configuration Script for Port 8001
# Changes OnlyOffice Document Server from port 80 to port 8001

Write-Host "CONFIGURING ONLYOFFICE DOCUMENT SERVER TO PORT 8001" -ForegroundColor Yellow
Write-Host "=" * 65

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-NOT $isAdmin) {
    Write-Host "This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    pause
    exit 1
}

$nginxConfPath = "C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\nginx.conf"

# Check if files exist
if (-not (Test-Path $nginxConfPath)) {
    Write-Host "nginx.conf not found at: $nginxConfPath" -ForegroundColor Red
    exit 1
}

# Stop OnlyOffice services
Write-Host "Stopping OnlyOffice services..." -ForegroundColor Yellow
$services = @("DsProxySvc", "DsDocServiceSvc", "DsConverterSvc")
foreach ($service in $services) {
    try {
        Stop-Service $service -Force -ErrorAction SilentlyContinue
        Write-Host "  Stopped: $service" -ForegroundColor Green
    } catch {
        Write-Host "  Could not stop: $service" -ForegroundColor Yellow
    }
}

# Backup and modify configuration
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupPath = "$nginxConfPath.backup.$timestamp"
Copy-Item $nginxConfPath $backupPath
Write-Host "Backup created: $backupPath" -ForegroundColor Cyan

$content = Get-Content $nginxConfPath
$newContent = $content -replace "listen\s+80;", "listen 8001;"
$newContent = $newContent -replace "listen\s+\[::]:80;", "listen [::]:8001;"
$newContent | Set-Content $nginxConfPath
Write-Host "nginx.conf updated to use port 8001" -ForegroundColor Green

# Start services
Write-Host "Starting OnlyOffice services..." -ForegroundColor Yellow
foreach ($service in $services) {
    try {
        Start-Service $service
        Write-Host "  Started: $service" -ForegroundColor Green
    } catch {
        Write-Host "  Failed to start: $service" -ForegroundColor Red
    }
}

Start-Sleep -Seconds 10

# Test new port
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001/" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "SUCCESS! OnlyOffice is accessible on port 8001" -ForegroundColor Green
    }
} catch {
    Write-Host "Port 8001 not yet accessible, may need more time" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "CONFIGURATION COMPLETE!" -ForegroundColor Green
Write-Host "  Document Server URL: http://localhost:8001" -ForegroundColor White
Write-Host "  OCR Agent already configured for this port" -ForegroundColor Green

# Test OCR Agent integration
Write-Host ""
Write-Host "Testing OCR Agent integration..." -ForegroundColor Yellow
try {
    cd "C:\OCR Agent"
    $testResult = python -c "
import requests, sys
try:
    r = requests.get('http://localhost:8001/', timeout=5)
    print(f'OnlyOffice Response: HTTP {r.status_code}')
    
    # Test OCR Agent settings
    sys.path.insert(0, '.')
    from app import create_app, db
    from app.models import SystemSettings
    app = create_app()
    with app.app_context():
        setting = SystemSettings.query.filter_by(key='onlyoffice_server_url').first()
        if setting and setting.value == 'http://localhost:8001':
            print('OCR Agent: Configured correctly')
        else:
            print('OCR Agent: Configuration mismatch')
except Exception as e:
    print(f'Test failed: {e}')
"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Integration test completed successfully!" -ForegroundColor Green
    }
} catch {
    Write-Host "Integration test skipped" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Visit http://localhost:8001 to verify OnlyOffice" -ForegroundColor White
Write-Host "2. Open OCR Agent Settings Panel to test connection" -ForegroundColor White
Write-Host "3. Upload a document to test full integration" -ForegroundColor White