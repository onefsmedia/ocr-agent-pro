# OnlyOffice Bootstrap Token Generator
# Restarts admin service and captures bootstrap token

Write-Host "🔧 ONLYOFFICE BOOTSTRAP TOKEN GENERATOR" -ForegroundColor Yellow
Write-Host "======================================="

# Check admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-NOT $isAdmin) {
    Write-Host "❌ ERROR: Administrator privileges required!" -ForegroundColor Red
    Write-Host "💡 Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    exit 1
}

Write-Host "`n🛑 Stopping OnlyOffice Admin Panel service..." -ForegroundColor Cyan
try {
    Stop-Service DsAdminPanelSvc -Force
    Write-Host "✅ Service stopped successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not stop service: $_" -ForegroundColor Yellow
}

Write-Host "`n⏳ Waiting 3 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 3

Write-Host "`n🚀 Starting OnlyOffice Admin Panel service..." -ForegroundColor Cyan
try {
    Start-Service DsAdminPanelSvc
    Write-Host "✅ Service started successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Could not start service: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n⏳ Waiting for service to initialize (10 seconds)..." -ForegroundColor Gray
Start-Sleep -Seconds 10

Write-Host "`n🔍 Checking for bootstrap token in logs..." -ForegroundColor Yellow

# Check multiple log locations
$logPaths = @(
    "C:\Program Files\ONLYOFFICE\DocumentServer\Log",
    "C:\Windows\Logs",
    "C:\ProgramData\ONLYOFFICE"
)

$found = $false

foreach ($logPath in $logPaths) {
    if (Test-Path $logPath) {
        Write-Host "`n📂 Searching in: $logPath" -ForegroundColor Cyan
        
        Get-ChildItem $logPath -Filter "*.log" -Recurse -ErrorAction SilentlyContinue | 
        Sort-Object LastWriteTime -Descending | 
        Select-Object -First 10 | 
        ForEach-Object {
            try {
                $recent = Get-Content $_.FullName -Tail 50 -ErrorAction SilentlyContinue
                $tokenLines = $recent | Select-String -Pattern "bootstrap.*token|admin.*token|token.*[a-zA-Z0-9]{8,}" -SimpleMatch $false
                
                if ($tokenLines) {
                    Write-Host "🎯 FOUND in $($_.Name):" -ForegroundColor Green
                    $tokenLines | ForEach-Object {
                        $line = $_.Line.Trim()
                        # Look for token patterns
                        if ($line -match "token[:\s=]+([a-zA-Z0-9]+)") {
                            Write-Host "   🔑 BOOTSTRAP TOKEN: $($matches[1])" -ForegroundColor Yellow -BackgroundColor DarkGreen
                            $found = $true
                        } else {
                            Write-Host "   $line" -ForegroundColor White
                        }
                    }
                }
            } catch {
                # Skip unreadable files
            }
        }
    }
}

if (-not $found) {
    Write-Host "`n❌ Bootstrap token not found in logs" -ForegroundColor Red
    Write-Host "`n💡 ALTERNATIVE SOLUTIONS:" -ForegroundColor Yellow
    Write-Host "==============================" 
    
    Write-Host "`n🎯 Option 1: Try common default tokens:" -ForegroundColor Cyan
    $defaultTokens = @("onlyoffice", "admin", "bootstrap", "docserver", "token123", "setup")
    foreach ($token in $defaultTokens) {
        Write-Host "   • $token" -ForegroundColor White
    }
    
    Write-Host "`n🎯 Option 2: Generate UUID-style token:" -ForegroundColor Cyan
    $uuid = [System.Guid]::NewGuid().ToString("N").Substring(0, 16)
    Write-Host "   • $uuid" -ForegroundColor Yellow
    
    Write-Host "`n🎯 Option 3: Check Windows Event Logs:" -ForegroundColor Cyan
    try {
        $events = Get-WinEvent -FilterHashtable @{LogName='Application'} -MaxEvents 50 | 
                  Where-Object {$_.Message -like "*onlyoffice*" -or $_.Message -like "*bootstrap*"}
        
        if ($events) {
            Write-Host "   Found OnlyOffice events in Application log" -ForegroundColor Green
            $events | Select-Object -First 3 | ForEach-Object {
                Write-Host "   $($_.TimeCreated): $($_.Message.Substring(0, [Math]::Min(100, $_.Message.Length)))..." -ForegroundColor Gray
            }
        } else {
            Write-Host "   No relevant events found" -ForegroundColor Gray
        }
    } catch {
        Write-Host "   Could not access Event Log" -ForegroundColor Gray
    }
}

Write-Host "`n🌐 NEXT STEPS:" -ForegroundColor Green
Write-Host "============="
Write-Host "1. Go back to: http://localhost:9000/" -ForegroundColor White
Write-Host "2. Try the bootstrap tokens shown above" -ForegroundColor White
Write-Host "3. Use any password you want for admin setup" -ForegroundColor White
Write-Host "4. If all tokens fail, try running this script again" -ForegroundColor White

Write-Host "`n⚠️ IF STILL STUCK:" -ForegroundColor Yellow
Write-Host "================"
Write-Host "• Check OnlyOffice documentation for your version" -ForegroundColor White
Write-Host "• Contact OnlyOffice support" -ForegroundColor White
Write-Host "• Consider reinstalling OnlyOffice Document Server" -ForegroundColor White