# OnlyOffice Admin Panel Access Script
# Starts admin services and provides access information

Write-Host "🔧 ONLYOFFICE ADMIN PANEL SETUP" -ForegroundColor Yellow
Write-Host "==============================="

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-NOT $isAdmin) {
    Write-Host "⚠️  This script requires Administrator privileges to start services!" -ForegroundColor Yellow
    Write-Host "💡 Please run PowerShell as Administrator for full functionality." -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "📊 Current OnlyOffice service status:" -ForegroundColor Cyan
Get-Service -Name "Ds*" | Where-Object {$_.Name -match "Admin|Example|Proxy|Doc|Convert"} | Format-Table Name,Status -AutoSize

if ($isAdmin) {
    # Start admin panel service
    Write-Host "`n🚀 Starting OnlyOffice Admin Panel service..." -ForegroundColor Yellow
    try {
        $adminService = Get-Service DsAdminPanelSvc -ErrorAction SilentlyContinue
        if ($adminService -and $adminService.Status -ne "Running") {
            Start-Service DsAdminPanelSvc
            Write-Host "✅ DsAdminPanelSvc started" -ForegroundColor Green
        } elseif ($adminService) {
            Write-Host "✅ DsAdminPanelSvc already running" -ForegroundColor Green
        } else {
            Write-Host "❌ DsAdminPanelSvc not found" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Failed to start DsAdminPanelSvc: $_" -ForegroundColor Red
    }

    # Start example service (often contains admin interface)
    Write-Host "`n🚀 Starting OnlyOffice Example service..." -ForegroundColor Yellow
    try {
        $exampleService = Get-Service DsExampleSvc -ErrorAction SilentlyContinue
        if ($exampleService -and $exampleService.Status -ne "Running") {
            Start-Service DsExampleSvc
            Write-Host "✅ DsExampleSvc started" -ForegroundColor Green
        } elseif ($exampleService) {
            Write-Host "✅ DsExampleSvc already running" -ForegroundColor Green
        } else {
            Write-Host "❌ DsExampleSvc not found" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Failed to start DsExampleSvc: $_" -ForegroundColor Red
    }

    Start-Sleep -Seconds 5
    
    Write-Host "`n📊 Updated service status:" -ForegroundColor Cyan
    Get-Service -Name "Ds*" | Where-Object {$_.Name -match "Admin|Example|Proxy|Doc|Convert"} | Format-Table Name,Status -AutoSize
}

# Test common OnlyOffice admin panel ports and endpoints
Write-Host "`n🔍 Scanning for OnlyOffice admin interfaces..." -ForegroundColor Yellow

$commonPorts = @(80, 443, 8000, 8080, 8443, 9001, 5432)
$adminEndpoints = @("/", "/welcome", "/example", "/healthcheck", "/admin")

foreach ($port in $commonPorts) {
    Write-Host "`n🔗 Testing port $port..." -ForegroundColor Cyan
    
    foreach ($endpoint in $adminEndpoints) {
        try {
            $url = "http://localhost:$port$endpoint"
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3 -ErrorAction SilentlyContinue
            
            $content = $response.Content.ToLower()
            
            # Check if this looks like OnlyOffice
            if ($content -match "onlyoffice|document.*server|editor|admin.*panel") {
                Write-Host "🎯 ONLYOFFICE FOUND: $url" -ForegroundColor Green
                Write-Host "   Status: HTTP $($response.StatusCode)" -ForegroundColor White
                Write-Host "   Size: $($response.Content.Length) bytes" -ForegroundColor White
                
                # Check specifically for admin features
                if ($content -match "admin|configuration|settings") {
                    Write-Host "   🔧 ADMIN INTERFACE DETECTED!" -ForegroundColor Yellow
                }
            } elseif ($response.StatusCode -eq 200) {
                Write-Host "✅ $endpoint - HTTP $($response.StatusCode) (not OnlyOffice)" -ForegroundColor Gray
            }
        } catch {
            # Silently skip failed connections
        }
    }
}

Write-Host "`n📋 ONLYOFFICE ADMIN PANEL ACCESS GUIDE" -ForegroundColor Green
Write-Host "======================================"

Write-Host "`n🎯 Common Admin Panel URLs to try:" -ForegroundColor Cyan
Write-Host "   • http://localhost/welcome" -ForegroundColor White
Write-Host "   • http://localhost/example" -ForegroundColor White  
Write-Host "   • http://localhost:8000/welcome" -ForegroundColor White
Write-Host "   • http://localhost:8443/welcome" -ForegroundColor White

Write-Host "`n🔧 Default Admin Credentials:" -ForegroundColor Cyan
Write-Host "   • Usually no authentication on first setup" -ForegroundColor White
Write-Host "   • Some installations use admin/admin" -ForegroundColor White
Write-Host "   • Check installation logs for auto-generated passwords" -ForegroundColor White

Write-Host "`n💡 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Try the URLs above in your web browser" -ForegroundColor White
Write-Host "   2. Look for 'Admin Panel' or 'Settings' links" -ForegroundColor White  
Write-Host "   3. Check OnlyOffice documentation for your version" -ForegroundColor White
Write-Host "   4. Enable admin services if they are stopped" -ForegroundColor White

Write-Host "`n🔍 If admin panel is not accessible:" -ForegroundColor Yellow
Write-Host "   • Run this script as Administrator" -ForegroundColor White
Write-Host "   • Check OnlyOffice installation logs" -ForegroundColor White
Write-Host "   • Verify all services are running" -ForegroundColor White
Write-Host "   • Consider reinstalling OnlyOffice Document Server" -ForegroundColor White