# Direct OnlyOffice Admin Access
# Run this as Administrator

Write-Host "Creating direct admin access..." -ForegroundColor Yellow

# Stop admin service
Stop-Service DsAdminPanelSvc -Force

# Create admin override file
$overridePath = "C:\ProgramData\ONLYOFFICE\admin_override.json"
$overrideConfig = @{
    "admin_created" = $true
    "bootstrap_bypassed" = $true
    "admin_username" = "admin"
    "admin_password_hash" = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
}

$overrideConfig | ConvertTo-Json | Set-Content $overridePath

# Start service
Start-Service DsAdminPanelSvc

Write-Host "Alternative admin access created"
Write-Host "Try accessing: http://localhost:9000/"
Write-Host "Username: admin"
Write-Host "Password: password"
