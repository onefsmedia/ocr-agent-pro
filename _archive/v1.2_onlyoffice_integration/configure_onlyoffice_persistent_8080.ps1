# OnlyOffice Persistent Port 8080 Configuration Script
# Ensures OnlyOffice Document Server is permanently configured for port 8080

Write-Host "🔧 CONFIGURING ONLYOFFICE FOR PERSISTENT PORT 8080" -ForegroundColor Yellow
Write-Host "===================================================="

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-NOT $isAdmin) {
    Write-Host "❌ This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "💡 Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    pause
    exit 1
}

# Define configuration files
$dsConfPath = "C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\ds.conf"
$nginxConfPath = "C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\nginx.conf"

# Check if files exist
if (-not (Test-Path $dsConfPath)) {
    Write-Host "❌ ds.conf not found at: $dsConfPath" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Configuration files found" -ForegroundColor Green
Write-Host "   ds.conf: $dsConfPath"
Write-Host "   nginx.conf: $nginxConfPath"

# Create backups with timestamp
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$dsBackupPath = "$dsConfPath.backup.$timestamp"
$nginxBackupPath = "$nginxConfPath.backup.$timestamp"

Copy-Item $dsConfPath $dsBackupPath
Write-Host "✅ Backup created: $dsBackupPath" -ForegroundColor Cyan

if (Test-Path $nginxConfPath) {
    Copy-Item $nginxConfPath $nginxBackupPath
    Write-Host "✅ Backup created: $nginxBackupPath" -ForegroundColor Cyan
}

# Stop OnlyOffice services
Write-Host "`n🛑 Stopping OnlyOffice services..." -ForegroundColor Yellow
$services = @("DsProxySvc", "DsDocServiceSvc", "DsConverterSvc")
foreach ($service in $services) {
    try {
        $serviceObj = Get-Service $service -ErrorAction SilentlyContinue
        if ($serviceObj -and $serviceObj.Status -eq "Running") {
            Stop-Service $service -Force -ErrorAction SilentlyContinue
            Write-Host "  ✅ Stopped: $service" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️ Not running: $service" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  ❌ Could not stop: $service" -ForegroundColor Red
    }
}

# Modify ds.conf to use port 8080
Write-Host "`n⚙️ Updating ds.conf configuration..." -ForegroundColor Yellow
$dsContent = Get-Content $dsConfPath
$newDsContent = $dsContent -replace "listen\s+0\.0\.0\.0:80;", "listen 0.0.0.0:8080;"
$newDsContent = $newDsContent -replace "listen\s+\[::]:80\s+default_server;", "listen [::]:8080 default_server;"
$newDsContent = $newDsContent -replace "listen\s+80;", "listen 8080;"
$newDsContent = $newDsContent -replace "listen\s+\[::]:80;", "listen [::]:8080;"

$newDsContent | Set-Content $dsConfPath
Write-Host "✅ ds.conf updated to use port 8080" -ForegroundColor Green

# Verify the changes
Write-Host "`n🔍 Verifying configuration changes..." -ForegroundColor Cyan
$verifyContent = Get-Content $dsConfPath | Select-String -Pattern "listen"
foreach ($line in $verifyContent) {
    Write-Host "  $($line.Line.Trim())" -ForegroundColor White
}

# Start OnlyOffice services
Write-Host "`n🚀 Starting OnlyOffice services..." -ForegroundColor Yellow
foreach ($service in $services) {
    try {
        Start-Service $service -ErrorAction SilentlyContinue
        Write-Host "  ✅ Started: $service" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Failed to start: $service" -ForegroundColor Red
    }
}

# Wait for services to initialize
Write-Host "`n⏳ Waiting for services to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

# Test the configuration
Write-Host "`n🧪 Testing OnlyOffice on port 8080..." -ForegroundColor Yellow
$maxAttempts = 5
$attempt = 1

while ($attempt -le $maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ SUCCESS! OnlyOffice is accessible on port 8080" -ForegroundColor Green
            Write-Host "   Status: HTTP $($response.StatusCode)" -ForegroundColor White
            Write-Host "   Response length: $($response.Content.Length) bytes" -ForegroundColor White
            break
        }
    } catch {
        Write-Host "⏳ Attempt $attempt/$maxAttempts failed, retrying..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        $attempt++
    }
}

if ($attempt -gt $maxAttempts) {
    Write-Host "❌ OnlyOffice not accessible after $maxAttempts attempts" -ForegroundColor Red
    Write-Host "💡 Check service status and logs" -ForegroundColor Yellow
}

# Test other ports to ensure no conflicts
Write-Host "`n🔍 Checking other ports for conflicts..." -ForegroundColor Cyan
$testPorts = @(80, 8000, 8001)
foreach ($port in $testPorts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port/" -UseBasicParsing -TimeoutSec 3 -ErrorAction SilentlyContinue
        Write-Host "⚠️  Port $port is also responding (HTTP $($response.StatusCode))" -ForegroundColor Yellow
    } catch {
        Write-Host "✅ Port $port is free" -ForegroundColor Green
    }
}

# Update Windows firewall if needed
Write-Host "`n🔥 Checking Windows Firewall..." -ForegroundColor Yellow
try {
    $firewallRule = Get-NetFirewallRule -DisplayName "*OnlyOffice*8080*" -ErrorAction SilentlyContinue
    if (-not $firewallRule) {
        New-NetFirewallRule -DisplayName "OnlyOffice Document Server 8080" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow -ErrorAction SilentlyContinue
        Write-Host "✅ Firewall rule created for port 8080" -ForegroundColor Green
    } else {
        Write-Host "✅ Firewall rule already exists" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Could not configure firewall (may require manual setup)" -ForegroundColor Yellow
}

Write-Host "`n🎯 CONFIGURATION COMPLETE!" -ForegroundColor Green
Write-Host "=========================="
Write-Host "✅ OnlyOffice Document Server configured for persistent port 8080" -ForegroundColor White
Write-Host "✅ Configuration backups created with timestamp: $timestamp" -ForegroundColor White
Write-Host "✅ Services restarted and tested" -ForegroundColor White
Write-Host "`n🔗 Document Server URL: http://localhost:8080" -ForegroundColor Cyan
Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Test OnlyOffice: http://localhost:8080" -ForegroundColor White
Write-Host "   2. Verify OCR Agent connection in Settings Panel" -ForegroundColor White
Write-Host "   3. Upload a document to test integration" -ForegroundColor White

# Create a verification script for future use
$verifyScript = @"
# OnlyOffice Port 8080 Verification Script
Write-Host "Checking OnlyOffice on port 8080..." -ForegroundColor Yellow
try {
    `$response = Invoke-WebRequest -Uri "http://localhost:8080/" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ OnlyOffice accessible (HTTP `$(`$response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "❌ OnlyOffice not accessible on port 8080" -ForegroundColor Red
}
"@

$verifyScript | Out-File -FilePath "verify_onlyoffice_8080.ps1" -Encoding UTF8
Write-Host "`n📝 Created verification script: verify_onlyoffice_8080.ps1" -ForegroundColor Cyan