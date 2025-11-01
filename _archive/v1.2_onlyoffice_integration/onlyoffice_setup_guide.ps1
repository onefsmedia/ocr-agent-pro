# OnlyOffice Admin Panel Setup Guide
# Complete step-by-step setup process

Write-Host "🎯 ONLYOFFICE ADMIN PANEL SETUP GUIDE" -ForegroundColor Green
Write-Host "====================================="

Write-Host "`n📋 STEP-BY-STEP SETUP PROCESS" -ForegroundColor Yellow
Write-Host "=============================="

Write-Host "`n1️⃣ BOOTSTRAP TOKEN OPTIONS:" -ForegroundColor Cyan
Write-Host "   Try these methods in order:" -ForegroundColor White
Write-Host "   • OPTION A: Leave bootstrap token field EMPTY (most common)" -ForegroundColor Green
Write-Host "   • OPTION B: Try 'onlyoffice' as the token" -ForegroundColor Yellow
Write-Host "   • OPTION C: Try 'admin' as the token" -ForegroundColor Yellow

Write-Host "`n2️⃣ ADMIN PASSWORD:" -ForegroundColor Cyan
Write-Host "   • Create a strong password (8+ characters)" -ForegroundColor White
Write-Host "   • Include letters, numbers, and symbols" -ForegroundColor White
Write-Host "   • Example: AdminPass2025!" -ForegroundColor Green

Write-Host "`n3️⃣ SETUP PROCESS:" -ForegroundColor Cyan
Write-Host "   1. Try leaving Bootstrap Token EMPTY first" -ForegroundColor White
Write-Host "   2. Enter your desired admin password" -ForegroundColor White
Write-Host "   3. Confirm the password" -ForegroundColor White
Write-Host "   4. Click SETUP button" -ForegroundColor White

Write-Host "`n🔧 IF EMPTY TOKEN DOESN'T WORK:" -ForegroundColor Yellow
Write-Host "==============================="

Write-Host "Method 1 - Restart admin service:" -ForegroundColor Cyan
Write-Host "   Stop-Service DsAdminPanelSvc" -ForegroundColor White
Write-Host "   Start-Service DsAdminPanelSvc" -ForegroundColor White
Write-Host "   (Then refresh browser and try again)" -ForegroundColor Gray

Write-Host "`nMethod 2 - Check for generated token:" -ForegroundColor Cyan

# Check for recently generated tokens
$logDir = "C:\Program Files\ONLYOFFICE\DocumentServer\Log"
if (Test-Path $logDir) {
    Write-Host "   Checking recent logs for token..." -ForegroundColor White
    
    $recentLogs = Get-ChildItem $logDir -Filter "*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 3
    
    foreach ($log in $recentLogs) {
        try {
            $content = Get-Content $log.FullName -Tail 50 | Select-String -Pattern "token|bootstrap|admin.*panel" -SimpleMatch $false
            if ($content) {
                Write-Host "   ✅ Found in $($log.Name):" -ForegroundColor Green
                $content | Select-Object -First 2 | ForEach-Object {
                    $line = $_.Line -replace '\s+', ' '
                    if ($line.Length -gt 80) { $line = $line.Substring(0, 80) + "..." }
                    Write-Host "      $line" -ForegroundColor Gray
                }
            }
        } catch {
            # Skip unreadable files
        }
    }
}

Write-Host "`n💡 RECOMMENDED APPROACH:" -ForegroundColor Green
Write-Host "======================="
Write-Host "1. Leave Bootstrap Token field EMPTY" -ForegroundColor White
Write-Host "2. Enter password: AdminPass2025!" -ForegroundColor White
Write-Host "3. Confirm password: AdminPass2025!" -ForegroundColor White
Write-Host "4. Click SETUP" -ForegroundColor White

Write-Host "`n🎉 AFTER SUCCESSFUL SETUP:" -ForegroundColor Green
Write-Host "========================="
Write-Host "• You'll be redirected to the main admin dashboard" -ForegroundColor White
Write-Host "• Configure your OnlyOffice Document Server settings" -ForegroundColor White
Write-Host "• Set up storage, authentication, and integrations" -ForegroundColor White
Write-Host "• Test document editing functionality" -ForegroundColor White

Write-Host "`n🔗 CURRENT ADMIN PANEL: http://localhost:9000/" -ForegroundColor Cyan

Write-Host "`n⚠️ TROUBLESHOOTING:" -ForegroundColor Yellow
Write-Host "=================="
Write-Host "If setup fails:" -ForegroundColor White
Write-Host "• Check service status: Get-Service DsAdminPanelSvc" -ForegroundColor Gray
Write-Host "• Restart services if needed" -ForegroundColor Gray
Write-Host "• Check Windows Firewall for port 9000" -ForegroundColor Gray
Write-Host "• Try different browsers (Chrome, Firefox, Edge)" -ForegroundColor Gray