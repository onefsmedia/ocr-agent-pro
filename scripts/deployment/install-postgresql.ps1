# PostgreSQL Quick Setup for Windows
# Alternative to Docker when Docker Desktop has issues

# Method 1: Download and Install PostgreSQL
Write-Host "PostgreSQL Installation Options:" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

Write-Host "Option 1: Official PostgreSQL Installer (Recommended)" -ForegroundColor Yellow
Write-Host "1. Download from: https://www.postgresql.org/download/windows/"
Write-Host "2. Run installer, set password for 'postgres' user"
Write-Host "3. Default port: 5432"
Write-Host "4. Remember the password!"
Write-Host ""

Write-Host "Option 2: Using Chocolatey" -ForegroundColor Yellow
Write-Host "Run as Administrator:"
Write-Host "choco install postgresql --params '/Password:admin123'"
Write-Host ""

Write-Host "Option 3: Using winget" -ForegroundColor Yellow
Write-Host "winget install PostgreSQL.PostgreSQL"
Write-Host ""

Write-Host "After Installation:" -ForegroundColor Cyan
Write-Host "1. Open Command Prompt as Administrator"
Write-Host "2. Run the setup commands below"
Write-Host ""

# PostgreSQL setup commands
$setupCommands = @"
-- Connect to PostgreSQL (you'll be prompted for password)
-- psql -U postgres -h localhost

-- Create the OCR database and user
CREATE USER ocr_user WITH PASSWORD 'ocr_password';
CREATE DATABASE ocr_agent OWNER ocr_user;
GRANT ALL PRIVILEGES ON DATABASE ocr_agent TO ocr_user;

-- Switch to the new database
\c ocr_agent

-- Install pgvector extension (if available)
CREATE EXTENSION IF NOT EXISTS vector;

-- Grant permissions
GRANT ALL ON SCHEMA public TO ocr_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ocr_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ocr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ocr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ocr_user;
"@

Write-Host "SQL Commands to run after installation:" -ForegroundColor Cyan
Write-Host $setupCommands

Write-Host ""
Write-Host "Quick Test Command:" -ForegroundColor Green
Write-Host "psql -U ocr_user -h localhost -d ocr_agent"