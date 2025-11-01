# OCR Agent Pro - PowerShell Setup Script
# Advanced setup and management for PowerShell users

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   OCR Agent Pro - PowerShell Manager" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

function Show-Menu {
    Write-Host "[1] Install Dependencies" -ForegroundColor Yellow
    Write-Host "[2] Test Direct Server" -ForegroundColor Yellow
    Write-Host "[3] Install Windows Service" -ForegroundColor Yellow
    Write-Host "[4] Start Service" -ForegroundColor Green
    Write-Host "[5] Stop Service" -ForegroundColor Red
    Write-Host "[6] Service Status" -ForegroundColor Blue
    Write-Host "[7] Uninstall Service" -ForegroundColor Red
    Write-Host "[8] View Logs (Live)" -ForegroundColor Magenta
    Write-Host "[9] Complete Setup" -ForegroundColor Cyan
    Write-Host "[10] Open Application" -ForegroundColor Green
    Write-Host "[0] Exit" -ForegroundColor Gray
    Write-Host ""
}

function Install-Dependencies {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    
    # Upgrade pip
    python -m pip install --upgrade pip
    
    # Install requirements
    if (Test-Path "requirements.txt") {
        python -m pip install -r requirements.txt
    } else {
        Write-Host "⚠️  requirements.txt not found, installing basic dependencies..." -ForegroundColor Yellow
        python -m pip install flask sqlalchemy psycopg2-binary requests waitress pillow
    }
    
    # Install Windows service support
    python -m pip install pywin32
    
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
    Read-Host "Press Enter to continue"
}

function Test-Server {
    Write-Host "Starting OCR Agent server directly (Press Ctrl+C to stop)..." -ForegroundColor Yellow
    python persistent_server.py
}

function Install-Service {
    Write-Host "Installing Windows Service..." -ForegroundColor Yellow
    
    try {
        python windows_service.py install
        Write-Host "✅ Service installed successfully!" -ForegroundColor Green
        Write-Host "   The service will automatically start on system boot." -ForegroundColor Cyan
    }
    catch {
        Write-Host "❌ Service installation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Read-Host "Press Enter to continue"
}

function Start-OCRService {
    Write-Host "Starting OCR Agent Pro service..." -ForegroundColor Yellow
    
    try {
        python windows_service.py start
        Write-Host "✅ Service started successfully!" -ForegroundColor Green
        Write-Host "🌐 Access your application at: http://localhost:5000" -ForegroundColor Cyan
    }
    catch {
        Write-Host "❌ Service start failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Read-Host "Press Enter to continue"
}

function Stop-OCRService {
    Write-Host "Stopping OCR Agent Pro service..." -ForegroundColor Yellow
    
    try {
        python windows_service.py stop
        Write-Host "✅ Service stopped successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Service stop failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Read-Host "Press Enter to continue"
}

function Get-ServiceStatus {
    Write-Host "Checking service status..." -ForegroundColor Yellow
    python windows_service.py status
    Read-Host "Press Enter to continue"
}

function Uninstall-Service {
    Write-Host "Uninstalling Windows Service..." -ForegroundColor Yellow
    
    $confirm = Read-Host "Are you sure you want to uninstall the service? (y/N)"
    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        try {
            python windows_service.py uninstall
            Write-Host "✅ Service uninstalled successfully!" -ForegroundColor Green
        }
        catch {
            Write-Host "❌ Service uninstall failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "Uninstall cancelled." -ForegroundColor Yellow
    }
    
    Read-Host "Press Enter to continue"
}

function Show-Logs {
    Write-Host "Viewing live logs (Press Ctrl+C to stop)..." -ForegroundColor Yellow
    Write-Host ""
    
    # Show recent logs first
    if (Test-Path "logs\service.log") {
        Write-Host "=== Recent Service Logs ===" -ForegroundColor Cyan
        Get-Content "logs\service.log" -Tail 10
        Write-Host ""
    }
    
    if (Test-Path "logs\server.log") {
        Write-Host "=== Recent Server Logs ===" -ForegroundColor Cyan
        Get-Content "logs\server.log" -Tail 10
        Write-Host ""
    }
    
    # Start live monitoring
    Write-Host "=== Live Log Monitoring ===" -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Yellow
    
    try {
        if (Test-Path "logs\service.log") {
            Get-Content "logs\service.log" -Wait
        } else {
            Write-Host "No logs found. Service may not be running." -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Log monitoring stopped." -ForegroundColor Yellow
    }
}

function Complete-Setup {
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "   Complete OCR Agent Pro Setup" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "Step 1: Installing dependencies..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    
    if (Test-Path "requirements.txt") {
        python -m pip install -r requirements.txt
    } else {
        python -m pip install flask sqlalchemy psycopg2-binary requests waitress pillow
    }
    
    python -m pip install pywin32
    
    Write-Host "Step 2: Installing Windows service..." -ForegroundColor Yellow
    python windows_service.py install
    
    Write-Host "Step 3: Starting service..." -ForegroundColor Yellow
    python windows_service.py start
    
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "   🎉 Setup Complete!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ OCR Agent Pro is now running as a Windows service" -ForegroundColor Green
    Write-Host "✅ Service will auto-start on system boot" -ForegroundColor Green
    Write-Host "✅ Access your application at: http://localhost:5000" -ForegroundColor Green
    Write-Host ""
    Write-Host "Service Management:" -ForegroundColor Cyan
    Write-Host "  • View logs: Option 8 from main menu" -ForegroundColor White
    Write-Host "  • Stop service: Option 5 from main menu" -ForegroundColor White
    Write-Host "  • Check status: Option 6 from main menu" -ForegroundColor White
    Write-Host ""
    
    Read-Host "Press Enter to continue"
}

function Open-Application {
    Write-Host "Opening OCR Agent Pro in your default browser..." -ForegroundColor Yellow
    Start-Process "http://localhost:5000"
}

# Main loop
do {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   OCR Agent Pro - PowerShell Manager" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    Show-Menu
    $choice = Read-Host "Select option (0-10)"
    
    switch ($choice) {
        "1" { Install-Dependencies }
        "2" { Test-Server }
        "3" { Install-Service }
        "4" { Start-OCRService }
        "5" { Stop-OCRService }
        "6" { Get-ServiceStatus }
        "7" { Uninstall-Service }
        "8" { Show-Logs }
        "9" { Complete-Setup }
        "10" { Open-Application }
        "0" { 
            Write-Host ""
            Write-Host "Goodbye! 👋" -ForegroundColor Green
            exit 
        }
        default { 
            Write-Host "Invalid option. Please try again." -ForegroundColor Red
            Start-Sleep 2
        }
    }
} while ($true)