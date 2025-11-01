#!/usr/bin/env python3
"""
OnlyOffice Alternative Port Scanner
Find the best available port for OnlyOffice Document Server
"""

import socket
import requests
import sys
import os

def check_port_availability(port):
    """Check if a port is available for binding"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            return result != 0  # Port is available if connection fails
    except:
        return False

def check_port_response(port):
    """Check if a port is responding to HTTP requests"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=2)
        return True, response.status_code
    except:
        return False, None

def find_best_onlyoffice_port():
    """Find the best available port for OnlyOffice Document Server"""
    
    print("🔍 SCANNING FOR BEST ONLYOFFICE PORT")
    print("=" * 45)
    
    # Preferred ports in order of preference
    preferred_ports = [8000, 8001, 8002, 8003, 8004, 8005, 9000, 9001, 9002, 8096, 8090]
    
    # Ports to avoid (commonly used by other services)
    avoid_ports = [8080]  # Apache/Tomcat commonly uses 8080
    
    available_ports = []
    busy_ports = []
    
    print("📡 Testing port availability...")
    
    for port in preferred_ports:
        if port in avoid_ports:
            print(f"  Port {port}: Skipped (commonly used by other services)")
            continue
            
        is_available = check_port_availability(port)
        is_responding, status_code = check_port_response(port)
        
        if is_available and not is_responding:
            available_ports.append(port)
            print(f"  Port {port}: ✅ Available")
        elif is_responding:
            busy_ports.append((port, status_code))
            print(f"  Port {port}: ❌ In use (HTTP {status_code})")
        else:
            print(f"  Port {port}: ❌ In use")
    
    print(f"\n📊 SCAN RESULTS:")
    print("-" * 25)
    
    if available_ports:
        recommended_port = available_ports[0]
        print(f"✅ Recommended port: {recommended_port}")
        print(f"✅ Available ports: {', '.join(map(str, available_ports))}")
        
        if busy_ports:
            print(f"❌ Busy ports: {', '.join([f'{p}(HTTP {s})' for p, s in busy_ports])}")
        
        return recommended_port, available_ports
    else:
        print("❌ No preferred ports available!")
        print("💡 Recommendations:")
        print("   - Use a higher port number (e.g., 18000, 28000)")
        print("   - Check what's using the preferred ports")
        print("   - Consider stopping conflicting services")
        return None, []

def update_ocr_agent_config(port):
    """Update OCR Agent configuration with the new port"""
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
        from app import create_app, db
        from app.models import SystemSettings
        
        app = create_app()
        
        with app.app_context():
            print(f"\n🔧 UPDATING OCR AGENT FOR PORT {port}")
            print("-" * 35)
            
            new_url = f"http://localhost:{port}"
            
            # Update or create the setting
            setting = SystemSettings.query.filter_by(key='onlyoffice_server_url').first()
            if setting:
                old_url = setting.value
                setting.value = new_url
                print(f"✅ Updated onlyoffice_server_url")
                print(f"   From: {old_url}")
                print(f"   To:   {new_url}")
            else:
                new_setting = SystemSettings(
                    key='onlyoffice_server_url',
                    value=new_url,
                    setting_type='string',
                    description='OnlyOffice Document Server URL'
                )
                db.session.add(new_setting)
                print(f"✅ Created onlyoffice_server_url: {new_url}")
            
            db.session.commit()
            return True
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def create_port_migration_script(target_port):
    """Create a PowerShell script for the recommended port"""
    
    script_content = f'''# OnlyOffice Port Configuration Script for Port {target_port}
# Changes OnlyOffice Document Server from port 80 to port {target_port}

Write-Host "CONFIGURING ONLYOFFICE DOCUMENT SERVER TO PORT {target_port}" -ForegroundColor Yellow
Write-Host "=" * 65

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-NOT $isAdmin) {{
    Write-Host "This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    pause
    exit 1
}}

$nginxConfPath = "C:\\Program Files\\ONLYOFFICE\\DocumentServer\\nginx\\conf\\nginx.conf"

# Check if files exist
if (-not (Test-Path $nginxConfPath)) {{
    Write-Host "nginx.conf not found at: $nginxConfPath" -ForegroundColor Red
    exit 1
}}

# Stop OnlyOffice services
Write-Host "Stopping OnlyOffice services..." -ForegroundColor Yellow
$services = @("DsProxySvc", "DsDocServiceSvc", "DsConverterSvc")
foreach ($service in $services) {{
    try {{
        Stop-Service $service -Force -ErrorAction SilentlyContinue
        Write-Host "  Stopped: $service" -ForegroundColor Green
    }} catch {{
        Write-Host "  Could not stop: $service" -ForegroundColor Yellow
    }}
}}

# Backup and modify configuration
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupPath = "$nginxConfPath.backup.$timestamp"
Copy-Item $nginxConfPath $backupPath
Write-Host "Backup created: $backupPath" -ForegroundColor Cyan

$content = Get-Content $nginxConfPath
$newContent = $content -replace "listen\\s+80;", "listen {target_port};"
$newContent = $newContent -replace "listen\\s+\\[::]:80;", "listen [::]:{target_port};"
$newContent | Set-Content $nginxConfPath
Write-Host "nginx.conf updated to use port {target_port}" -ForegroundColor Green

# Start services
Write-Host "Starting OnlyOffice services..." -ForegroundColor Yellow
foreach ($service in $services) {{
    try {{
        Start-Service $service
        Write-Host "  Started: $service" -ForegroundColor Green
    }} catch {{
        Write-Host "  Failed to start: $service" -ForegroundColor Red
    }}
}}

Start-Sleep -Seconds 10

# Test new port
try {{
    $response = Invoke-WebRequest -Uri "http://localhost:{target_port}/" -UseBasicParsing -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {{
        Write-Host "SUCCESS! OnlyOffice is accessible on port {target_port}" -ForegroundColor Green
    }}
}} catch {{
    Write-Host "Port {target_port} not yet accessible, may need more time" -ForegroundColor Yellow
}}

Write-Host ""
Write-Host "CONFIGURATION COMPLETE!" -ForegroundColor Green
Write-Host "  Document Server URL: http://localhost:{target_port}" -ForegroundColor White
'''
    
    script_filename = f"configure_onlyoffice_port_{target_port}.ps1"
    with open(script_filename, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\n📝 Created migration script: {script_filename}")
    return script_filename

if __name__ == "__main__":
    # Find the best available port
    recommended_port, available_ports = find_best_onlyoffice_port()
    
    if recommended_port:
        print(f"\n🎯 RECOMMENDATION: Use port {recommended_port}")
        print("=" * 40)
        
        # Update OCR Agent configuration
        config_success = update_ocr_agent_config(recommended_port)
        
        # Create migration script
        script_file = create_port_migration_script(recommended_port)
        
        print(f"\n🚀 NEXT STEPS:")
        print("-" * 15)
        print(f"1. Run PowerShell as Administrator")
        print(f"2. Execute: .\\{script_file}")
        print(f"3. Test: http://localhost:{recommended_port}")
        print(f"4. Verify OCR Agent connection in Settings Panel")
        
        if config_success:
            print("\n✅ OCR Agent already configured for the new port!")
        
    else:
        print("\n❌ No suitable ports found")
        print("💡 Consider using a custom high port (e.g., 18000)")