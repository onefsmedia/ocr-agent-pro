#!/usr/bin/env python3
"""
Configure OCR Agent to work with local OnlyOffice Document Server
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import SystemSettings

def configure_onlyoffice_url():
    """Configure OnlyOffice URL for local installation"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 CONFIGURING ONLYOFFICE DOCUMENT SERVER")
        print("=" * 50)
        
        # Test different possible URLs
        test_urls = [
            'http://localhost',
            'http://localhost:80', 
            'http://127.0.0.1',
            'http://127.0.0.1:80'
        ]
        
        import requests
        working_url = None
        
        for url in test_urls:
            try:
                print(f"Testing {url}...")
                response = requests.get(f"{url}/healthcheck", timeout=5)
                if response.status_code == 200:
                    working_url = url
                    print(f"✅ Found working URL: {url}")
                    break
                else:
                    print(f"   Status: {response.status_code}")
            except Exception as e:
                print(f"   Error: {str(e)[:50]}...")
        
        if not working_url:
            print("❌ OnlyOffice Document Server not responding on standard ports")
            print("💡 Recommendations:")
            print("   1. Check if OnlyOffice Document Server services are running")
            print("   2. Check Windows Firewall settings")
            print("   3. Try accessing http://localhost in your browser")
            return False
        
        # Update settings
        settings_to_update = {
            'onlyoffice_server_url': working_url,
            'onlyoffice_enabled': 'true',
            'onlyoffice_mode': 'document_server'
        }
        
        for key, value in settings_to_update.items():
            setting = SystemSettings.query.filter_by(key=key).first()
            if setting:
                setting.value = value
                print(f"✅ Updated {key}: {value}")
            else:
                new_setting = SystemSettings(
                    key=key,
                    value=value,
                    setting_type='string',
                    description=f'OnlyOffice configuration: {key}'
                )
                db.session.add(new_setting)
                print(f"✅ Created {key}: {value}")
        
        db.session.commit()
        print("\n🎉 OnlyOffice configuration updated!")
        print(f"📍 Document Server URL: {working_url}")
        print("🌐 Test it in OCR Agent settings panel")
        
        return True

if __name__ == "__main__":
    success = configure_onlyoffice_url()
    if success:
        print("\n🚀 Next steps:")
        print("1. Open OCR Agent: http://localhost:5000")
        print("2. Go to Settings: http://localhost:5000/panel/settings")
        print("3. Test OnlyOffice connection")
    else:
        print("\n🔧 Troubleshooting needed for OnlyOffice Document Server")