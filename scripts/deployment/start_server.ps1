# OCR Agent Pro Server Launcher
# PowerShell script for stable server startup

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    OCR Agent Pro Server Launcher" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set location
Set-Location "c:\OCR Agent"

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python." -ForegroundColor Red
    exit 1
}

# Check if required files exist
if (-not (Test-Path "app.py")) {
    Write-Host "❌ app.py not found in current directory" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Starting OCR Agent Pro..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor White
Write-Host "  🌐 http://localhost:5000" -ForegroundColor Cyan
Write-Host "  🌐 http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "🛑 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server using Start-Process to avoid signal handling issues
$process = Start-Process python -ArgumentList "app.py" -PassThru -NoNewWindow

# Wait for process
try {
    $process.WaitForExit()
} catch {
    Write-Host "Server interrupted" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🛑 Server stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"