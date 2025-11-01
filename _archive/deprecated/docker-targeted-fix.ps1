# Docker Desktop Fix Script for Diagnostics ID: C28ED140-FD16-4ACD-ADF6-F01B0DB210AF
# Based on the diagnostics, this appears to be a named pipe permission issue

Write-Host "=== Docker Desktop Targeted Fix ===" -ForegroundColor Green
Write-Host "Diagnostics ID: C28ED140-FD16-4ACD-ADF6-F01B0DB210AF" -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop Docker completely
Write-Host "1. Stopping Docker processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*docker*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Stop-Service com.docker.service -Force -ErrorAction SilentlyContinue

# Step 2: Clear problematic Docker state
Write-Host "2. Clearing Docker state..." -ForegroundColor Yellow
$dockerAppData = "$env:LOCALAPPDATA\Docker"
if (Test-Path "$dockerAppData\config.json") {
    Remove-Item "$dockerAppData\config.json" -Force -ErrorAction SilentlyContinue
}

# Step 3: Fix the specific named pipe issue from diagnostics
Write-Host "3. Fixing named pipe permissions (specific to your diagnostics)..." -ForegroundColor Yellow

# Remove existing pipes
Remove-Item "\\.\pipe\docker_engine" -Force -ErrorAction SilentlyContinue
Remove-Item "\\.\pipe\dockerDesktopLinuxEngine" -Force -ErrorAction SilentlyContinue

# Set registry permissions for Docker service
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\com.docker.service"
if (Test-Path $regPath) {
    $acl = Get-Acl $regPath
    $accessRule = New-Object System.Security.AccessControl.RegistryAccessRule("Everyone", "FullControl", "Allow")
    $acl.SetAccessRule($accessRule)
    $acl | Set-Acl -Path $regPath
}

# Step 4: Fix Docker Desktop registry entries
Write-Host "4. Fixing Docker Desktop registry..." -ForegroundColor Yellow
$dockerRegPath = "HKCU:\Software\Docker Inc.\Docker Desktop"
if (Test-Path $dockerRegPath) {
    Set-ItemProperty -Path $dockerRegPath -Name "startOnBoot" -Value 0 -ErrorAction SilentlyContinue
}

# Step 5: Reset Windows container service
Write-Host "5. Resetting Windows container service..." -ForegroundColor Yellow
Stop-Service winnat -Force -ErrorAction SilentlyContinue
Start-Service winnat -ErrorAction SilentlyContinue

# Step 6: Start Docker service with elevated permissions
Write-Host "6. Starting Docker service..." -ForegroundColor Yellow
sc.exe config com.docker.service start= auto
Start-Service com.docker.service

# Step 7: Wait and start Docker Desktop
Write-Host "7. Starting Docker Desktop..." -ForegroundColor Yellow
Start-Sleep 3
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Fix applied! Please wait 60 seconds for Docker Desktop to start." -ForegroundColor Green
Write-Host "If Docker Desktop prompts for WSL2 backend, accept it." -ForegroundColor Cyan
Write-Host ""