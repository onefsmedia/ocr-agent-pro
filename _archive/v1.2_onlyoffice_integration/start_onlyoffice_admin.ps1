# Start OnlyOffice Admin Panel Services
# Requires Administrator privileges

Write-Host "Starting OnlyOffice Admin Panel Services..." -ForegroundColor Yellow

# Check admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-NOT $isAdmin) {
    Write-Host "ERROR: Administrator privileges required!" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator." -ForegroundColor Yellow
    exit 1
}

# Start admin panel service
try {
    Write-Host "Starting DsAdminPanelSvc..." -ForegroundColor Cyan
    Start-Service DsAdminPanelSvc
    Write-Host "✅ DsAdminPanelSvc started" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to start DsAdminPanelSvc: $_" -ForegroundColor Red
}

# Start example service
try {
    Write-Host "Starting DsExampleSvc..." -ForegroundColor Cyan
    Start-Service DsExampleSvc
    Write-Host "✅ DsExampleSvc started" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to start DsExampleSvc: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 5

Write-Host "`nService Status:" -ForegroundColor Yellow
Get-Service DsAdminPanelSvc,DsExampleSvc | Format-Table Name,Status -AutoSize

Write-Host "`nTesting admin panel access..." -ForegroundColor Yellow
$adminUrls = @(
    "http://localhost/welcome",
    "http://localhost/example", 
    "http://localhost:8000/welcome",
    "http://localhost:8080/welcome"
)

foreach ($url in $adminUrls) {
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
        Write-Host "✅ FOUND: $url (HTTP $($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "❌ $url - Not accessible" -ForegroundColor Red
    }
}

Write-Host "`nAdmin Panel Access Information:" -ForegroundColor Green
Write-Host "• Check the accessible URLs above in your web browser"
Write-Host "• Look for welcome pages or example interfaces"
Write-Host "• Admin panel may be integrated into the main interface"