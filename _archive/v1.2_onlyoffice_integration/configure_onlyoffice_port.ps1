# OnlyOffice Port Configuration Script
# Changes OnlyOffice Document Server from port 80 to port 8096

Write-Host "CONFIGURING ONLYOFFICE DOCUMENT SERVER PORT" -ForegroundColor Yellow
Write-Host "=" * 60

$nginxConfPath = "C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\nginx.conf"
$dsConfPath = "C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\ds.conf"

# Check if files exist
if (-not (Test-Path $nginxConfPath)) {
    Write-Host "nginx.conf not found at: $nginxConfPath" -ForegroundColor Red
    exit 1
}

# Stop OnlyOffice services first
Write-Host "Stopping OnlyOffice services..." -ForegroundColor Yellow
try {
    Stop-Service "ONLYOFFICE Document Server Converter" -Force -ErrorAction SilentlyContinue
    Stop-Service "ONLYOFFICE Document Server DocService" -Force -ErrorAction SilentlyContinue
    Stop-Service "ONLYOFFICE Document Server Proxy" -Force -ErrorAction SilentlyContinue
    Write-Host "Services stopped" -ForegroundColor Green
} catch {
    Write-Host "Some services may already be stopped" -ForegroundColor Yellow
}

# Backup original configuration
$backupPath = "$nginxConfPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $nginxConfPath $backupPath
Write-Host "Backup created: $backupPath" -ForegroundColor Cyan

# Read current configuration
$content = Get-Content $nginxConfPath

# Replace port 80 with 8096
$newContent = $content -replace "listen\s+80;", "listen 8096;"
$newContent = $newContent -replace "listen\s+\[::]:80;", "listen [::]:8096;"

# Write back the configuration
$newContent | Set-Content $nginxConfPath

Write-Host "nginx.conf updated to use port 8096" -ForegroundColor Green

# Also check and update ds.conf if it exists
if (Test-Path $dsConfPath) {
    $backupDsPath = "$dsConfPath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $dsConfPath $backupDsPath
    
    $dsContent = Get-Content $dsConfPath
    $newDsContent = $dsContent -replace "listen\s+80;", "listen 8096;"
    $newDsContent = $newDsContent -replace "listen\s+\[::]:80;", "listen [::]:8096;"
    $newDsContent | Set-Content $dsConfPath
    
    Write-Host "ds.conf updated to use port 8096" -ForegroundColor Green
}

# Start services back up
Write-Host "Starting OnlyOffice services..." -ForegroundColor Yellow
try {
    Start-Service "ONLYOFFICE Document Server Proxy" -ErrorAction SilentlyContinue
    Start-Service "ONLYOFFICE Document Server DocService" -ErrorAction SilentlyContinue  
    Start-Service "ONLYOFFICE Document Server Converter" -ErrorAction SilentlyContinue
    Write-Host "Services started" -ForegroundColor Green
} catch {
    Write-Host "Some services may need manual restart" -ForegroundColor Yellow
}

# Wait a moment for services to start
Start-Sleep -Seconds 5

# Test the new port
Write-Host "Testing new port configuration..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8096/welcome" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "SUCCESS! OnlyOffice Document Server is now accessible on port 8096!" -ForegroundColor Green
    } else {
        Write-Host "Port 8096 responding with status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Port 8096 not yet accessible, may need a few more seconds to start" -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "ONLYOFFICE PORT CONFIGURATION COMPLETE!" -ForegroundColor Green
Write-Host "   • Port changed from 80 to 8096" -ForegroundColor White
Write-Host "   • Backup created: $backupPath" -ForegroundColor White
Write-Host "   • New URL: http://localhost:8096" -ForegroundColor White
Write-Host ""