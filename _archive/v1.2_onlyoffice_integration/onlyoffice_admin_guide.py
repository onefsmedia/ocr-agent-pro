"""
OnlyOffice Document Server Admin Panel Access Guide
==================================================

Based on the configuration analysis, here's how to access the OnlyOffice admin panel:

ADMIN PANEL CONFIGURATION FOUND:
• Admin Panel Port: 9000 (from default.json)
• Document Server Port: 8080 (currently running)
• Services Required: DsAdminPanelSvc (currently stopped)

STEPS TO ACCESS ADMIN PANEL:

1. START ADMIN PANEL SERVICE (Requires Administrator)
   Run PowerShell as Administrator and execute:
   Start-Service DsAdminPanelSvc

2. ACCESS ADMIN PANEL
   Open your web browser and navigate to:
   http://localhost:9000/

3. ALTERNATIVE ACCESS METHODS
   If port 9000 doesn't work, try these URLs:
   • http://localhost:9000/welcome
   • http://localhost:9000/admin
   • http://localhost:8080/welcome (if integrated with main server)

CURRENT SERVICE STATUS:
• DsProxySvc: ✅ Running (main proxy)
• DsDocServiceSvc: ✅ Running (document service)
• DsConverterSvc: ✅ Running (converter service)
• DsAdminPanelSvc: ❌ Stopped (admin panel - NEEDS TO BE STARTED)
• DsExampleSvc: ❌ Stopped (example interface)

TROUBLESHOOTING:

If admin panel is not accessible:
1. Ensure you have Administrator privileges
2. Start the admin panel service manually
3. Check Windows Firewall for port 9000
4. Verify OnlyOffice logs for errors

ALTERNATIVE ADMIN ACCESS:

If the web admin panel doesn't work, you can configure OnlyOffice through:
1. Configuration files in: C:\Program Files\ONLYOFFICE\DocumentServer\config\
2. Command line tools
3. Direct database access (PostgreSQL)

COMMON ADMIN TASKS:
• License management
• User authentication settings
• Storage configuration
• SSL/TLS settings
• Integration settings
• Performance monitoring

DEFAULT CREDENTIALS:
• Most OnlyOffice installations don't require authentication for admin panel
• Some installations use: admin/admin
• Check installation logs for auto-generated passwords
"""

import subprocess
import sys

def start_admin_service():
    """Attempt to start the admin service"""
    try:
        # Check if we're running as admin
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        
        if not is_admin:
            print("❌ Administrator privileges required to start services")
            print("💡 Run PowerShell as Administrator and execute:")
            print("   Start-Service DsAdminPanelSvc")
            return False
        
        # Start the service
        result = subprocess.run([
            'powershell', '-Command', 'Start-Service DsAdminPanelSvc'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ DsAdminPanelSvc started successfully")
            return True
        else:
            print(f"❌ Failed to start DsAdminPanelSvc: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        return False

def test_admin_access():
    """Test admin panel accessibility"""
    import requests
    
    admin_urls = [
        "http://localhost:9000/",
        "http://localhost:9000/welcome",
        "http://localhost:9000/admin"
    ]
    
    print("\n🔍 Testing admin panel access...")
    
    for url in admin_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ ADMIN PANEL FOUND: {url}")
                print(f"   Status: HTTP {response.status_code}")
                print(f"   Content Length: {len(response.text)} characters")
                return url
            else:
                print(f"⚠️  {url} - HTTP {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"❌ {url} - Not accessible")
    
    return None

if __name__ == "__main__":
    print(__doc__)
    
    print("\n🚀 ATTEMPTING TO START ADMIN SERVICE...")
    print("=" * 45)
    
    if start_admin_service():
        print("\n⏳ Waiting for service to initialize...")
        import time
        time.sleep(5)
        
        admin_url = test_admin_access()
        
        if admin_url:
            print(f"\n🎉 SUCCESS! Admin panel accessible at: {admin_url}")
            print("\n📋 Next steps:")
            print("1. Open your web browser")
            print(f"2. Navigate to: {admin_url}")
            print("3. Configure your OnlyOffice Document Server")
        else:
            print("\n❌ Admin panel not accessible")
            print("💡 Try accessing manually: http://localhost:9000/")
    else:
        print("\n💡 To manually start the admin service:")
        print("1. Open PowerShell as Administrator")
        print("2. Run: Start-Service DsAdminPanelSvc")
        print("3. Access: http://localhost:9000/")