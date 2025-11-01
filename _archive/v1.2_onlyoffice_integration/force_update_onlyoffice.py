#!/usr/bin/env python3
"""
Force update OnlyOffice settings and verify
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import SystemSettings

def force_update_settings():
    """Force update OnlyOffice settings"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 FORCE UPDATING ONLYOFFICE SETTINGS")
        print("=" * 50)
        
        # Clear and recreate settings
        settings_to_update = {
            'onlyoffice_server_url': 'http://localhost:80',
            'onlyoffice_enabled': 'true',
            'onlyoffice_mode': 'document_server',
            'onlyoffice_jwt_secret': 'ocr-agent-secret-key-2025'
        }
        
        for key, value in settings_to_update.items():
            # Delete existing setting
            existing = SystemSettings.query.filter_by(key=key).first()
            if existing:
                db.session.delete(existing)
                print(f"🗑️  Deleted old {key}")
            
            # Create new setting
            new_setting = SystemSettings(
                key=key,
                value=value,
                setting_type='string',
                description=f'OnlyOffice configuration: {key}'
            )
            db.session.add(new_setting)
            print(f"✅ Created {key}: {value}")
        
        db.session.commit()
        
        # Verify settings
        print("\n📋 Current OnlyOffice Settings:")
        for key in settings_to_update.keys():
            setting = SystemSettings.query.filter_by(key=key).first()
            if setting:
                print(f"   {key}: {setting.value}")
            else:
                print(f"   {key}: NOT FOUND")
        
        print("\n🎉 Settings force-updated!")
        print("💡 Please restart your Flask application to apply changes")
        
        return True

if __name__ == "__main__":
    force_update_settings()