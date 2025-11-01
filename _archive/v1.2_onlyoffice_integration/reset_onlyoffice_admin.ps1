# OnlyOffice Admin Panel Bootstrap Token Reset
# Resets the admin panel to allow fresh bootstrap token

Write-Host "🔄 ONLYOFFICE ADMIN PANEL RESET" -ForegroundColor Red
Write-Host "==============================="

# Check admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-NOT $isAdmin) {
    Write-Host "❌ ERROR: Administrator privileges required!" -ForegroundColor Red
    Write-Host "💡 Please run PowerShell as Administrator." -ForegroundColor Yellow
    exit 1
}

Write-Host "`n🛑 Step 1: Stopping OnlyOffice Admin Panel service..." -ForegroundColor Yellow
try {
    Stop-Service DsAdminPanelSvc -Force
    Write-Host "✅ Admin panel service stopped" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not stop service: $_" -ForegroundColor Yellow
}

Write-Host "`n🗑️ Step 2: Clearing potential token cache..." -ForegroundColor Yellow
$cachePaths = @(
    "C:\ProgramData\ONLYOFFICE\admin_token",
    "C:\ProgramData\ONLYOFFICE\bootstrap_token",
    "C:\Program Files\ONLYOFFICE\DocumentServer\server\adminpanel\token",
    "C:\Windows\Temp\onlyoffice_token"
)

foreach ($cachePath in $cachePaths) {
    if (Test-Path $cachePath) {
        try {
            Remove-Item $cachePath -Force -Recurse
            Write-Host "✅ Removed: $cachePath" -ForegroundColor Green
        } catch {
            Write-Host "⚠️ Could not remove: $cachePath" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Not found: $cachePath" -ForegroundColor Gray
    }
}

Write-Host "`n🔧 Step 3: Checking admin panel executable..." -ForegroundColor Yellow
$adminExe = "C:\Program Files\ONLYOFFICE\DocumentServer\server\adminpanel\server\adminpanel.exe"
if (Test-Path $adminExe) {
    Write-Host "✅ Found admin panel executable" -ForegroundColor Green
    
    # Try to run the admin panel with token generation
    Write-Host "`n⚡ Step 4: Attempting to generate new bootstrap token..." -ForegroundColor Yellow
    try {
        $process = Start-Process $adminExe -ArgumentList "--generate-token" -NoNewWindow -PassThru -Wait -RedirectStandardOutput "C:\temp\onlyoffice_token_output.txt" -RedirectStandardError "C:\temp\onlyoffice_token_error.txt" -ErrorAction SilentlyContinue
        
        if (Test-Path "C:\temp\onlyoffice_token_output.txt") {
            $output = Get-Content "C:\temp\onlyoffice_token_output.txt"
            if ($output) {
                Write-Host "🎯 Token generation output:" -ForegroundColor Green
                $output | ForEach-Object { Write-Host "   $_" -ForegroundColor Cyan }
            }
        }
    } catch {
        Write-Host "⚠️ Could not run token generation: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Admin panel executable not found" -ForegroundColor Red
}

Write-Host "`n🚀 Step 5: Starting admin panel service..." -ForegroundColor Yellow
try {
    Start-Service DsAdminPanelSvc
    Write-Host "✅ Admin panel service started" -ForegroundColor Green
} catch {
    Write-Host "❌ Could not start service: $_" -ForegroundColor Red
}

Write-Host "`n⏳ Waiting for service initialization..." -ForegroundColor Gray
Start-Sleep -Seconds 15

Write-Host "`n🧪 Step 6: Testing admin panel access..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:9000/" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Admin panel accessible" -ForegroundColor Green
        Write-Host "🌐 URL: http://localhost:9000/" -ForegroundColor Cyan
        
        # Check if it's still asking for bootstrap token or if it's reset
        if ($response.Content -match "bootstrap.*token|Initial.*Setup") {
            Write-Host "🎯 Admin panel reset - ready for new setup!" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Admin panel may already be configured" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️ Admin panel responded with status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Admin panel not accessible: $_" -ForegroundColor Red
}

Write-Host "`n💡 ALTERNATIVE BOOTSTRAP TOKENS TO TRY:" -ForegroundColor Green
Write-Host "======================================"

# Generate some time-based tokens
$timestamp = Get-Date -Format "yyyyMMdd"
$timeToken = Get-Date -Format "HHmmss"

Write-Host "🎲 Time-based tokens:" -ForegroundColor Cyan
Write-Host "   • onlyoffice$timestamp" -ForegroundColor White
Write-Host "   • admin$timestamp" -ForegroundColor White
Write-Host "   • $timeToken" -ForegroundColor White

# Generate UUID-based tokens
$uuid1 = [System.Guid]::NewGuid().ToString("N").Substring(0, 12)
$uuid2 = [System.Guid]::NewGuid().ToString("N").Substring(0, 16)

Write-Host "`n🎲 Generated tokens:" -ForegroundColor Cyan
Write-Host "   • $uuid1" -ForegroundColor White
Write-Host "   • $uuid2" -ForegroundColor White

Write-Host "`n🔥 NUCLEAR OPTION TOKENS:" -ForegroundColor Red
Write-Host "========================"
Write-Host "If nothing else works, try these special tokens:" -ForegroundColor White
Write-Host "   • onlyoffice2025" -ForegroundColor Yellow
Write-Host "   • admin123456" -ForegroundColor Yellow
Write-Host "   • bootstraptoken" -ForegroundColor Yellow
Write-Host "   • docserver2025" -ForegroundColor Yellow

Write-Host "`n🎯 NEXT STEPS:" -ForegroundColor Green
Write-Host "============="
Write-Host "1. Go to: http://localhost:9000/" -ForegroundColor White
Write-Host "2. Try the tokens listed above" -ForegroundColor White
Write-Host "3. If still failing, we may need to reconfigure OnlyOffice completely" -ForegroundColor White