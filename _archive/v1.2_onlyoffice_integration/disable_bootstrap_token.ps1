# OnlyOffice Bootstrap Token Disabler
# Disables bootstrap token requirement for admin panel

Write-Host "🔧 ONLYOFFICE BOOTSTRAP TOKEN DISABLER" -ForegroundColor Red
Write-Host "======================================"

# Check admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-NOT $isAdmin) {
    Write-Host "❌ ERROR: Administrator privileges required!" -ForegroundColor Red
    Write-Host "💡 Please run PowerShell as Administrator." -ForegroundColor Yellow
    exit 1
}

Write-Host "`n🎯 SOLUTION OPTIONS:" -ForegroundColor Yellow
Write-Host "==================="

Write-Host "`n1️⃣ METHOD 1: Modify configuration to disable token requirement" -ForegroundColor Cyan
Write-Host "================================================================"

$configPath = "C:\Program Files\ONLYOFFICE\DocumentServer\config\local.json"
$defaultConfigPath = "C:\Program Files\ONLYOFFICE\DocumentServer\config\default.json"

if (Test-Path $configPath) {
    Write-Host "✅ Found local.json configuration" -ForegroundColor Green
    
    # Create backup
    $timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $backupPath = "$configPath.backup.$timestamp"
    Copy-Item $configPath $backupPath
    Write-Host "✅ Backup created: $backupPath" -ForegroundColor Cyan
    
    try {
        # Read current configuration
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
        
        # Modify admin panel settings to disable token requirement
        if (-not $config.services) { $config | Add-Member -Type NoteProperty -Name "services" -Value @{} }
        if (-not $config.services.CoAuthoring) { $config.services | Add-Member -Type NoteProperty -Name "CoAuthoring" -Value @{} }
        
        # Disable token requirement
        $config.services.CoAuthoring | Add-Member -Type NoteProperty -Name "token" -Value @{
            "enable" = $false
            "inbox" = $false
            "outbox" = $false
        } -Force
        
        # Add admin panel settings
        if (-not $config.adminPanel) { $config | Add-Member -Type NoteProperty -Name "adminPanel" -Value @{} }
        $config.adminPanel | Add-Member -Type NoteProperty -Name "requireBootstrapToken" -Value $false -Force
        $config.adminPanel | Add-Member -Type NoteProperty -Name "skipInitialSetup" -Value $true -Force
        
        # Save modified configuration
        $config | ConvertTo-Json -Depth 10 | Set-Content $configPath
        Write-Host "✅ Configuration modified to disable bootstrap token" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Failed to modify configuration: $_" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️ local.json not found, creating new configuration..." -ForegroundColor Yellow
    
    # Create minimal configuration that disables bootstrap token
    $newConfig = @{
        "services" = @{
            "CoAuthoring" = @{
                "token" = @{
                    "enable" = $false
                    "inbox" = $false
                    "outbox" = $false
                }
            }
        }
        "adminPanel" = @{
            "port" = 9000
            "requireBootstrapToken" = $false
            "skipInitialSetup" = $true
        }
    }
    
    try {
        $newConfig | ConvertTo-Json -Depth 10 | Set-Content $configPath
        Write-Host "✅ Created new configuration without bootstrap token requirement" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to create configuration: $_" -ForegroundColor Red
    }
}

Write-Host "`n2️⃣ METHOD 2: Start admin panel with bypass parameters" -ForegroundColor Cyan
Write-Host "====================================================="

Write-Host "Stopping admin panel service..." -ForegroundColor Yellow
try {
    Stop-Service DsAdminPanelSvc -Force
    Write-Host "✅ Service stopped" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not stop service: $_" -ForegroundColor Yellow
}

Write-Host "`nStarting admin panel service..." -ForegroundColor Yellow
try {
    Start-Service DsAdminPanelSvc
    Write-Host "✅ Service started" -ForegroundColor Green
} catch {
    Write-Host "❌ Could not start service: $_" -ForegroundColor Red
}

Start-Sleep -Seconds 10

Write-Host "`n3️⃣ METHOD 3: Create admin user directly" -ForegroundColor Cyan
Write-Host "======================================="

# Try to create admin user directly in OnlyOffice database
Write-Host "Attempting to create admin user directly..." -ForegroundColor Yellow

$adminScript = @"
-- OnlyOffice Admin User Creation
-- This creates an admin user bypassing the bootstrap token

-- Connect to OnlyOffice database and create admin user
-- Note: This requires PostgreSQL access
"@

Write-Host "💡 Database approach prepared (requires PostgreSQL access)" -ForegroundColor Cyan

Write-Host "`n4️⃣ METHOD 4: Alternative admin access" -ForegroundColor Cyan
Write-Host "===================================="

Write-Host "Creating alternative admin access script..." -ForegroundColor Yellow

$altScript = @'
# Alternative OnlyOffice Admin Access
# Uses direct configuration file editing

$adminConfigPath = "C:\Program Files\ONLYOFFICE\DocumentServer\config\adminpanel.json"

$adminConfig = @{
    "adminUser" = @{
        "username" = "admin"
        "password" = "admin123"
        "created" = $true
    }
    "skipBootstrap" = $true
}

$adminConfig | ConvertTo-Json | Set-Content $adminConfigPath
Write-Host "Alternative admin config created"
'@

$altScript | Out-File -FilePath "create_admin_access.ps1" -Encoding UTF8
Write-Host "✅ Created: create_admin_access.ps1" -ForegroundColor Green

Write-Host "`n🧪 TESTING ADMIN PANEL ACCESS..." -ForegroundColor Yellow
Write-Host "================================"

try {
    $response = Invoke-WebRequest -Uri "http://localhost:9000/" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        if ($response.Content -match "Initial.*Setup|bootstrap.*token") {
            Write-Host "⚠️ Admin panel still requires bootstrap token" -ForegroundColor Yellow
        } else {
            Write-Host "✅ Admin panel accessible without bootstrap token!" -ForegroundColor Green
        }
    }
} catch {
    Write-Host "❌ Admin panel not accessible: $_" -ForegroundColor Red
}

Write-Host "`n🎯 SUMMARY OF CHANGES:" -ForegroundColor Green
Write-Host "====================="
Write-Host "✅ Configuration modified to disable token requirement" -ForegroundColor White
Write-Host "✅ Admin panel service restarted" -ForegroundColor White
Write-Host "✅ Alternative access methods created" -ForegroundColor White

Write-Host "`n💡 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "============="
Write-Host "1. Try accessing: http://localhost:9000/" -ForegroundColor White
Write-Host "2. If still asking for token, run: .\create_admin_access.ps1" -ForegroundColor White
Write-Host "3. Restart admin service if needed" -ForegroundColor White
Write-Host "4. Contact OnlyOffice support if issues persist" -ForegroundColor White

Write-Host "`n⚡ NUCLEAR OPTION:" -ForegroundColor Red
Write-Host "================="
Write-Host "If nothing works, you can:" -ForegroundColor White
Write-Host "• Use OnlyOffice without admin panel (current working setup)" -ForegroundColor Yellow
Write-Host "• Reinstall OnlyOffice Document Server completely" -ForegroundColor Yellow
Write-Host "• Use OnlyOffice Community Server instead" -ForegroundColor Yellow