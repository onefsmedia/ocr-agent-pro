#!/usr/bin/env python3
"""
Update OCR Agent Pro configuration for OnlyOffice port 8096
"""

import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app
from app.models import SystemSettings

def update_onlyoffice_port():
    """Update OnlyOffice configuration for port 8096"""
    print("🔧 UPDATING OCR AGENT PRO - ONLYOFFICE PORT CONFIGURATION")
    print("=" * 60)
    
    app = create_app()
    with app.app_context():
        try:
            # Update OnlyOffice server URL to use port 8096
            server_url_setting = SystemSettings.query.filter_by(key='onlyoffice_server_url').first()
            if server_url_setting:
                old_url = server_url_setting.value
                server_url_setting.value = 'http://localhost:8096'
                print(f"✅ Updated onlyoffice_server_url: {old_url} → http://localhost:8096")
            else:
                # Create new setting if it doesn't exist
                new_setting = SystemSettings(
                    key='onlyoffice_server_url',
                    value='http://localhost:8096',
                    description='OnlyOffice Document Server URL',
                    setting_type='string'
                )
                from app import db
                db.session.add(new_setting)
                print("✅ Created onlyoffice_server_url: http://localhost:8096")
            
            # Ensure document server mode is enabled
            mode_setting = SystemSettings.query.filter_by(key='onlyoffice_mode').first()
            if mode_setting:
                mode_setting.value = 'document_server'
                print(f"✅ Confirmed onlyoffice_mode: {mode_setting.value}")
            
            # Update API endpoint
            api_endpoint_setting = SystemSettings.query.filter_by(key='onlyoffice_api_endpoint').first()
            if api_endpoint_setting:
                old_endpoint = api_endpoint_setting.value
                api_endpoint_setting.value = 'http://localhost:8096/coauthoring/CommandService.ashx'
                print(f"✅ Updated onlyoffice_api_endpoint: {old_endpoint} → http://localhost:8096/coauthoring/CommandService.ashx")
            else:
                new_setting = SystemSettings(
                    key='onlyoffice_api_endpoint',
                    value='http://localhost:8096/coauthoring/CommandService.ashx',
                    description='OnlyOffice API endpoint for document operations',
                    setting_type='string'
                )
                from app import db
                db.session.add(new_setting)
                print("✅ Created onlyoffice_api_endpoint: http://localhost:8096/coauthoring/CommandService.ashx")
            
            # Commit changes
            from app import db
            db.session.commit()
            
            print("\n🎉 OCR AGENT PRO CONFIGURATION UPDATED!")
            print("   • OnlyOffice server URL: http://localhost:8096")
            print("   • Mode: document_server")
            print("   • API endpoint: http://localhost:8096/coauthoring/CommandService.ashx")
            print("\n📝 Next steps:")
            print("   1. Run the admin script: configure_onlyoffice_port_admin.ps1 (as Administrator)")
            print("   2. Test OnlyOffice access: http://localhost:8096")
            print("   3. Start OCR Agent Pro to test integration")
            
        except Exception as e:
            print(f"❌ Error updating configuration: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    update_onlyoffice_port()