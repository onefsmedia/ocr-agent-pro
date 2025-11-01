#!/usr/bin/env python3
"""
OnlyOffice Port 8080 Persistence Monitor
Monitors and verifies OnlyOffice Document Server binding to port 8080
"""

import requests
import socket
import subprocess
import sys
import os
import time
from datetime import datetime

def check_port_binding(port):
    """Check if OnlyOffice is properly bound to the specified port"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', port))
            return result == 0  # Port is bound if connection succeeds
    except:
        return False

def test_onlyoffice_response(port):
    """Test if OnlyOffice is responding correctly on the port"""
    try:
        response = requests.get(f"http://localhost:{port}/", timeout=5)
        return True, response.status_code, len(response.text)
    except Exception as e:
        return False, None, str(e)

def check_nginx_config():
    """Check the nginx configuration for port settings"""
    try:
        ds_conf_path = r"C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\ds.conf"
        
        if os.path.exists(ds_conf_path):
            with open(ds_conf_path, 'r') as f:
                content = f.read()
                
            # Look for listen directives
            import re
            listen_lines = re.findall(r'listen\s+[^;]+;', content)
            return True, listen_lines
        else:
            return False, ["ds.conf not found"]
    except Exception as e:
        return False, [str(e)]

def check_onlyoffice_services():
    """Check OnlyOffice service status"""
    services = ["DsProxySvc", "DsDocServiceSvc", "DsConverterSvc"]
    service_status = {}
    
    for service in services:
        try:
            result = subprocess.run([
                'powershell', '-Command', 
                f'Get-Service -Name "{service}" | Select-Object -ExpandProperty Status'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                status = result.stdout.strip()
                service_status[service] = status
            else:
                service_status[service] = "Unknown"
        except:
            service_status[service] = "Error"
    
    return service_status

def update_ocr_agent_config(port):
    """Ensure OCR Agent is configured for the correct port"""
    try:
        sys.path.insert(0, '.')
        from app import create_app, db
        from app.models import SystemSettings
        
        app = create_app()
        with app.app_context():
            setting = SystemSettings.query.filter_by(key='onlyoffice_server_url').first()
            expected_url = f"http://localhost:{port}"
            
            if setting:
                if setting.value == expected_url:
                    return True, f"Already configured: {setting.value}"
                else:
                    old_url = setting.value
                    setting.value = expected_url
                    db.session.commit()
                    return True, f"Updated: {old_url} -> {expected_url}"
            else:
                new_setting = SystemSettings(
                    key='onlyoffice_server_url',
                    value=expected_url,
                    setting_type='string',
                    description='OnlyOffice Document Server URL'
                )
                db.session.add(new_setting)
                db.session.commit()
                return True, f"Created: {expected_url}"
    except Exception as e:
        return False, str(e)

def main():
    print("🔍 ONLYOFFICE PORT 8080 PERSISTENCE MONITOR")
    print("=" * 50)
    print(f"📅 Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    target_port = 8080
    
    # 1. Check port binding
    print("1️⃣ PORT BINDING CHECK")
    print("-" * 25)
    is_bound = check_port_binding(target_port)
    if is_bound:
        print(f"✅ Port {target_port} is bound and accessible")
    else:
        print(f"❌ Port {target_port} is not bound")
    
    # 2. Test OnlyOffice response
    print(f"\n2️⃣ ONLYOFFICE RESPONSE TEST")
    print("-" * 30)
    is_responding, status_code, response_info = test_onlyoffice_response(target_port)
    if is_responding:
        print(f"✅ OnlyOffice responding on port {target_port}")
        print(f"   HTTP Status: {status_code}")
        print(f"   Response size: {response_info} characters")
    else:
        print(f"❌ OnlyOffice not responding on port {target_port}")
        print(f"   Error: {response_info}")
    
    # 3. Check nginx configuration
    print(f"\n3️⃣ NGINX CONFIGURATION")
    print("-" * 25)
    config_ok, listen_directives = check_nginx_config()
    if config_ok:
        print("✅ ds.conf accessible")
        for directive in listen_directives:
            if "8080" in directive:
                print(f"✅ Found: {directive}")
            else:
                print(f"⚠️  Found: {directive}")
    else:
        print("❌ Could not read ds.conf")
        for error in listen_directives:
            print(f"   {error}")
    
    # 4. Check services
    print(f"\n4️⃣ SERVICE STATUS")
    print("-" * 20)
    services = check_onlyoffice_services()
    all_running = True
    for service, status in services.items():
        if status == "Running":
            print(f"✅ {service}: {status}")
        else:
            print(f"❌ {service}: {status}")
            all_running = False
    
    # 5. Update OCR Agent
    print(f"\n5️⃣ OCR AGENT CONFIGURATION")
    print("-" * 30)
    config_success, config_message = update_ocr_agent_config(target_port)
    if config_success:
        print(f"✅ {config_message}")
    else:
        print(f"❌ Configuration error: {config_message}")
    
    # 6. Overall status
    print(f"\n📊 OVERALL STATUS")
    print("-" * 20)
    if is_bound and is_responding and all_running and config_success:
        print("🎉 ALL SYSTEMS GO! OnlyOffice is persistently bound to port 8080")
        print("✅ Port binding: Working")
        print("✅ OnlyOffice response: Working") 
        print("✅ Services: Running")
        print("✅ OCR Agent config: Updated")
    else:
        print("⚠️  Some issues detected:")
        if not is_bound:
            print("   ❌ Port binding issue")
        if not is_responding:
            print("   ❌ OnlyOffice not responding")
        if not all_running:
            print("   ❌ Service status issue")
        if not config_success:
            print("   ❌ OCR Agent configuration issue")
    
    print(f"\n💡 RECOMMENDATIONS")
    print("-" * 20)
    if not (is_bound and is_responding):
        print("   • Run configure_onlyoffice_persistent_8080.ps1 as Administrator")
        print("   • Check OnlyOffice service logs")
        print("   • Verify nginx configuration")
    else:
        print("   • Configuration is persistent and working")
        print("   • Test document upload in OCR Agent")
        print("   • Monitor logs for any issues")

if __name__ == "__main__":
    main()