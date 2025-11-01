# OCR Agent Pro - Waitress Server Launcher
# PowerShell script for starting the production server

param(
    [switch]$Install,
    [switch]$Check,
    [switch]$Status,
    [switch]$Stop,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

function Write-Header {
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "   OCR Agent Pro - Waitress Production Server" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
}

function Test-Dependencies {
    Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Python not found!" -ForegroundColor Red
        return $false
    }
    
    # Check Waitress
    try {
        python -c "import waitress; print('Waitress installed')" 2>$null
        Write-Host "✅ Waitress: Available" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Waitress: Not installed" -ForegroundColor Yellow
        return $false
    }
    
    # Check Flask app
    try {
        python -c "from app import create_app; print('Flask app OK')" 2>$null
        Write-Host "✅ Flask App: Working" -ForegroundColor Green
    } catch {
        Write-Host "❌ Flask App: Error" -ForegroundColor Red
        return $false
    }
    
    return $true
}

function Install-Dependencies {
    Write-Host "📦 Installing Waitress..." -ForegroundColor Yellow
    try {
        python -m pip install waitress psycopg2-binary pillow
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        return $false
    }
    return $true
}

function Get-ServerStatus {
    $port5000 = netstat -ano | Select-String ":5000"
    if ($port5000) {
        Write-Host "🟢 Server Status: RUNNING on port 5000" -ForegroundColor Green
        Write-Host "🌐 Access URL: http://localhost:5000" -ForegroundColor Cyan
        return $true
    } else {
        Write-Host "🔴 Server Status: STOPPED" -ForegroundColor Red
        return $false
    }
}

function Stop-Server {
    Write-Host "🛑 Stopping OCR Agent Pro server..." -ForegroundColor Yellow
    try {
        Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force
        Write-Host "✅ Server stopped successfully" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  No Python processes found" -ForegroundColor Yellow
    }
}

function Start-Server {
    Write-Header
    
    # Check current directory
    if (-not (Test-Path "app.py")) {
        Write-Host "❌ Error: app.py not found!" -ForegroundColor Red
        Write-Host "Please run this script from the OCR Agent directory" -ForegroundColor Yellow
        return
    }
    
    # Check dependencies
    if (-not (Test-Dependencies)) {
        Write-Host ""
        Write-Host "Installing missing dependencies..." -ForegroundColor Yellow
        if (-not (Install-Dependencies)) {
            Write-Host "❌ Dependency installation failed!" -ForegroundColor Red
            return
        }
    }
    
    Write-Host ""
    Write-Host "🚀 Starting OCR Agent Pro with Waitress server..." -ForegroundColor Green
    Write-Host "🌐 Server URL: http://localhost:5000" -ForegroundColor Cyan
    Write-Host "🛑 Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Start the server
    try {
        python app.py
    } catch {
        Write-Host "❌ Server startup failed!" -ForegroundColor Red
    }
}

function Show-Help {
    Write-Header
    Write-Host "Usage: .\start_waitress.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "  -Install    Install required dependencies" -ForegroundColor White
    Write-Host "  -Check      Check system dependencies" -ForegroundColor White
    Write-Host "  -Status     Check if server is running" -ForegroundColor White
    Write-Host "  -Stop       Stop running server" -ForegroundColor White
    Write-Host "  -Help       Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\start_waitress.ps1          # Start server" -ForegroundColor White
    Write-Host "  .\start_waitress.ps1 -Check   # Check dependencies" -ForegroundColor White
    Write-Host "  .\start_waitress.ps1 -Status  # Check server status" -ForegroundColor White
}

# Main execution
if ($Help) {
    Show-Help
} elseif ($Install) {
    Write-Header
    Install-Dependencies
} elseif ($Check) {
    Write-Header
    Test-Dependencies
} elseif ($Status) {
    Write-Header
    Get-ServerStatus
} elseif ($Stop) {
    Write-Header
    Stop-Server
} else {
    Start-Server
}