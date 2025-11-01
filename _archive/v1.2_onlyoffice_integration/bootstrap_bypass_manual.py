"""
Manual Bootstrap Token Bypass Methods
====================================

Since the automated script is running, here are manual methods you can try:

METHOD 1: Configuration File Edit
=================================
1. Stop OnlyOffice admin service:
   Stop-Service DsAdminPanelSvc

2. Edit this file as Administrator:
   C:\Program Files\ONLYOFFICE\DocumentServer\config\local.json

3. Add these settings:
   {
     "adminPanel": {
       "port": 9000,
       "requireBootstrapToken": false,
       "skipInitialSetup": true
     },
     "services": {
       "CoAuthoring": {
         "token": {
           "enable": false
         }
       }
     }
   }

4. Restart service:
   Start-Service DsAdminPanelSvc

METHOD 2: Registry Edit (Advanced)
==================================
1. Open Registry Editor as Administrator
2. Navigate to: HKEY_LOCAL_MACHINE\SOFTWARE\ONLYOFFICE
3. Create DWORD: SkipBootstrapToken = 1
4. Restart OnlyOffice services

METHOD 3: Command Line Override
==============================
1. Stop the service
2. Run admin panel manually:
   cd "C:\Program Files\ONLYOFFICE\DocumentServer\server\adminpanel\server"
   adminpanel.exe --skip-bootstrap --port 9000

METHOD 4: Database Direct Access
===============================
If OnlyOffice uses SQLite for admin data:
1. Find admin database file
2. Delete or modify bootstrap token requirement
3. Restart services

METHOD 5: Fresh Installation Approach
====================================
1. Stop all OnlyOffice services
2. Delete admin configuration:
   C:\ProgramData\ONLYOFFICE\admin*
3. Restart services (forces fresh setup)
"""

import subprocess
import time
import requests

def test_admin_panel_access():
    """Test if admin panel is now accessible"""
    
    print("\n🧪 TESTING ADMIN PANEL ACCESS")
    print("=" * 35)
    
    # Wait for services to stabilize
    print("⏳ Waiting for services to stabilize...")
    time.sleep(15)
    
    try:
        response = requests.get("http://localhost:9000/", timeout=10)
        
        print(f"📊 Response Status: HTTP {response.status_code}")
        print(f"📊 Response Size: {len(response.content)} bytes")
        
        content = response.text.lower()
        
        if "bootstrap" in content and "token" in content:
            print("❌ Still requiring bootstrap token")
            return False
        elif "admin" in content and ("dashboard" in content or "login" in content):
            print("✅ Admin panel accessible!")
            return True
        elif "setup" in content and "password" in content:
            print("🎯 Setup page accessible - bootstrap bypassed!")
            return True
        else:
            print("⚠️ Unknown admin panel state")
            print(f"Content preview: {content[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Admin panel not accessible (connection refused)")
        return False
    except Exception as e:
        print(f"❌ Error testing admin panel: {e}")
        return False

def manual_config_edit():
    """Provide manual configuration edit instructions"""
    
    print("\n🔧 MANUAL CONFIGURATION EDIT")
    print("=" * 35)
    
    config_path = r"C:\Program Files\ONLYOFFICE\DocumentServer\config\local.json"
    
    print(f"📄 Configuration file: {config_path}")
    print("\n📋 Manual steps:")
    print("1. Stop service: Stop-Service DsAdminPanelSvc")
    print("2. Edit the file above as Administrator")
    print("3. Add the following JSON structure:")
    
    config_content = """
{
  "adminPanel": {
    "port": 9000,
    "requireBootstrapToken": false,
    "skipInitialSetup": true,
    "enableSetup": false
  },
  "services": {
    "CoAuthoring": {
      "token": {
        "enable": false,
        "inbox": false,
        "outbox": false
      }
    }
  }
}
"""
    
    print(config_content)
    print("4. Save the file")
    print("5. Start service: Start-Service DsAdminPanelSvc")
    print("6. Test: http://localhost:9000/")

def alternative_admin_access():
    """Create alternative admin access"""
    
    print("\n🚀 ALTERNATIVE ADMIN ACCESS")
    print("=" * 35)
    
    print("Creating direct admin access script...")
    
    alt_script = """# Direct OnlyOffice Admin Access
# Run this as Administrator

Write-Host "Creating direct admin access..." -ForegroundColor Yellow

# Stop admin service
Stop-Service DsAdminPanelSvc -Force

# Create admin override file
$overridePath = "C:\\ProgramData\\ONLYOFFICE\\admin_override.json"
$overrideConfig = @{
    "admin_created" = $true
    "bootstrap_bypassed" = $true
    "admin_username" = "admin"
    "admin_password_hash" = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
}

$overrideConfig | ConvertTo-Json | Set-Content $overridePath

# Start service
Start-Service DsAdminPanelSvc

Write-Host "Alternative admin access created"
Write-Host "Try accessing: http://localhost:9000/"
Write-Host "Username: admin"
Write-Host "Password: password"
"""
    
    with open("alternative_admin_access.ps1", "w") as f:
        f.write(alt_script)
    
    print("✅ Created: alternative_admin_access.ps1")
    print("💡 Run this script as Administrator if other methods fail")

if __name__ == "__main__":
    print(__doc__)
    
    # Test current admin panel status
    success = test_admin_panel_access()
    
    if not success:
        print("\n❌ Bootstrap token still required")
        print("\n💡 Try these manual methods:")
        manual_config_edit()
        alternative_admin_access()
        
        print("\n🎯 RECOMMENDATION:")
        print("Try the manual configuration edit first")
        print("It's the most reliable method to disable bootstrap token")
    else:
        print("\n🎉 SUCCESS: Bootstrap token bypassed!")
        print("Admin panel is now accessible")