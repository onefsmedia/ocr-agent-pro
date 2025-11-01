#!/usr/bin/env python3
"""
OnlyOffice Port Migration Helper
Helps transition OnlyOffice from port 80 to port 8000
"""

import requests
import time

def check_current_status():
    """Check what's currently running on various ports"""
    
    print("🔍 ONLYOFFICE PORT STATUS CHECK")
    print("=" * 40)
    
    ports_to_check = [80, 8000, 8080, 8096]
    results = {}
    
    for port in ports_to_check:
        print(f"Testing port {port}...")
        
        test_urls = [
            f"http://localhost:{port}/",
            f"http://localhost:{port}/welcome",
            f"http://localhost:{port}/healthcheck"
        ]
        
        port_status = "Not accessible"
        for url in test_urls:
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    content = response.text.lower()
                    if 'onlyoffice' in content or 'document server' in content:
                        port_status = "OnlyOffice Document Server"
                        break
                    else:
                        port_status = "Other web server"
                        break
            except:
                continue
        
        results[port] = port_status
        print(f"  Port {port}: {port_status}")
    
    print("\n📊 RESULTS SUMMARY:")
    print("-" * 30)
    
    onlyoffice_port = None
    for port, status in results.items():
        if "OnlyOffice" in status:
            onlyoffice_port = port
            print(f"✅ OnlyOffice found on port {port}")
            break
    
    if onlyoffice_port == 8000:
        print("🎉 OnlyOffice is already on port 8000!")
        return configure_ocr_agent()
    elif onlyoffice_port == 80:
        print("🔧 OnlyOffice is on port 80, needs migration to port 8000")
        return provide_migration_steps()
    elif onlyoffice_port:
        print(f"🔧 OnlyOffice is on port {onlyoffice_port}, needs migration to port 8000")
        return provide_migration_steps()
    else:
        print("❌ OnlyOffice Document Server not found on any port")
        return troubleshoot_onlyoffice()

def configure_ocr_agent():
    """Configure OCR Agent for port 8000"""
    
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
        
        from app import create_app, db
        from app.models import SystemSettings
        
        app = create_app()
        
        with app.app_context():
            # Update settings for port 8000
            setting = SystemSettings.query.filter_by(key='onlyoffice_server_url').first()
            if setting:
                setting.value = 'http://localhost:8000'
            else:
                new_setting = SystemSettings(
                    key='onlyoffice_server_url',
                    value='http://localhost:8000',
                    setting_type='string',
                    description='OnlyOffice Document Server URL'
                )
                db.session.add(new_setting)
            
            db.session.commit()
            print("✅ OCR Agent configured for port 8000")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
    
    print("\n🚀 READY TO USE!")
    print("  OnlyOffice URL: http://localhost:8000")
    print("  Test connection in OCR Agent Settings Panel")
    return True

def provide_migration_steps():
    """Provide migration instructions"""
    
    print("\n🔧 MIGRATION REQUIRED")
    print("=" * 30)
    print("OnlyOffice needs to be moved from port 80 to port 8000")
    print("")
    print("📋 Quick Migration Steps:")
    print("1. Open PowerShell AS ADMINISTRATOR")
    print("2. Navigate to: cd 'C:\\OCR Agent'")
    print("3. Run: .\\configure_port_8000_simple.ps1")
    print("")
    print("📖 OR follow manual guide:")
    print("   See: ONLYOFFICE_PORT_8000_MANUAL_GUIDE.md")
    print("")
    print("🔄 After migration, run this script again to verify")
    return False

def troubleshoot_onlyoffice():
    """Provide troubleshooting steps"""
    
    print("\n🛠️ TROUBLESHOOTING ONLYOFFICE")
    print("=" * 35)
    print("OnlyOffice Document Server services are installed but not responding")
    print("")
    print("🔧 Try these steps:")
    print("1. Check services: Get-Service Ds*")
    print("2. Restart services in Services.msc")
    print("3. Check Windows Firewall")
    print("4. Look for error logs in:")
    print("   C:\\Program Files\\ONLYOFFICE\\DocumentServer\\logs\\")
    print("")
    print("🔄 After fixing, run this script again")
    return False

if __name__ == "__main__":
    success = check_current_status()
    
    if success:
        print("\n🎉 OnlyOffice configuration complete!")
        print("   Test in OCR Agent: http://localhost:5000/panel/settings")
    else:
        print("\n⏳ Migration or troubleshooting needed")
        print("   Run this script again after completing the steps")