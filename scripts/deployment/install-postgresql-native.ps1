# Native PostgreSQL Installation Script for Windows
# This bypasses all container/WSL issues

Write-Host "=== Installing PostgreSQL Natively on Windows ===" -ForegroundColor Green
Write-Host "This avoids all Docker/Podman/WSL issues" -ForegroundColor Cyan
Write-Host ""

# Install PostgreSQL using Chocolatey (most reliable method)
Write-Host "Installing PostgreSQL with Chocolatey..." -ForegroundColor Yellow

# Check if Chocolatey is installed
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey first..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install PostgreSQL
Write-Host "Installing PostgreSQL..." -ForegroundColor Yellow
choco install postgresql15 --params '/Password:ocr_password' -y

# Wait for installation
Start-Sleep 10

# Add PostgreSQL to PATH
$pgPath = "C:\Program Files\PostgreSQL\15\bin"
if (Test-Path $pgPath) {
    $env:PATH += ";$pgPath"
    [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$pgPath", [EnvironmentVariableTarget]::Machine)
}

Write-Host ""
Write-Host "PostgreSQL installed! Now creating database..." -ForegroundColor Green

# Create database and user
$sqlCommands = @"
CREATE USER ocr_user WITH PASSWORD 'ocr_password';
CREATE DATABASE ocr_agent OWNER ocr_user;
GRANT ALL PRIVILEGES ON DATABASE ocr_agent TO ocr_user;
\c ocr_agent
GRANT ALL ON SCHEMA public TO ocr_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ocr_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ocr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ocr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ocr_user;
"@

$sqlCommands | Out-File -FilePath "setup_db.sql" -Encoding UTF8

# Run SQL setup
Write-Host "Setting up database..." -ForegroundColor Yellow
$env:PGPASSWORD = "ocr_password"
& "$pgPath\psql.exe" -U postgres -h localhost -f setup_db.sql

# Test connection
Write-Host ""
Write-Host "Testing connection..." -ForegroundColor Yellow
& "$pgPath\psql.exe" -U ocr_user -h localhost -d ocr_agent -c "SELECT version();"

Write-Host ""
Write-Host "PostgreSQL setup complete!" -ForegroundColor Green
Write-Host "Database: ocr_agent" -ForegroundColor Cyan
Write-Host "User: ocr_user" -ForegroundColor Cyan
Write-Host "Password: ocr_password" -ForegroundColor Cyan
Write-Host "Port: 5432" -ForegroundColor Cyan