#!/usr/bin/env python3
"""
OnlyOffice Configuration Script for OCR Agent Pro
Sets up OnlyOffice settings in the database
"""

from app import create_app, db
from app.models import SystemSettings

def configure_onlyoffice_settings():
    """Configure OnlyOffice settings for OCR Agent Pro"""
    
    app = create_app()
    
    with app.app_context():
        print('🔧 CONFIGURING ONLYOFFICE SETTINGS')
        print('=' * 50)
        
        # Set up OnlyOffice configuration
        onlyoffice_settings = {
            'onlyoffice_url': 'http://localhost:8000',
            'onlyoffice_secret': 'ocr-agent-secret-key-2025',
            'onlyoffice_token': '',
            'onlyoffice_storage_url': 'http://localhost:5000/storage',
            'onlyoffice_mode': 'local_files',
            'onlyoffice_enabled': 'false'
        }
        
        # Descriptions for each setting
        descriptions = {
            'onlyoffice_url': 'OnlyOffice Document Server URL',
            'onlyoffice_secret': 'OnlyOffice JWT Secret Key',
            'onlyoffice_token': 'OnlyOffice API Token',
            'onlyoffice_storage_url': 'OnlyOffice Storage URL',
            'onlyoffice_mode': 'OnlyOffice Integration Mode',
            'onlyoffice_enabled': 'OnlyOffice Integration Enabled'
        }
        
        # Save settings to database
        settings_updated = 0
        settings_created = 0
        
        for key, value in onlyoffice_settings.items():
            setting = SystemSettings.query.filter_by(key=key).first()
            
            if setting:
                setting.value = value
                settings_updated += 1
                print(f'   ✅ Updated: {key} = {value}')
            else:
                setting = SystemSettings(
                    key=key,
                    value=value,
                    description=descriptions.get(key, f'OnlyOffice setting: {key}'),
                    setting_type='string'
                )
                db.session.add(setting)
                settings_created += 1
                print(f'   ✅ Created: {key} = {value}')
        
        # Commit changes
        try:
            db.session.commit()
            print()
            print('✅ OnlyOffice settings saved successfully!')
            print(f'   📊 Updated: {settings_updated} settings')
            print(f'   📊 Created: {settings_created} settings')
            
        except Exception as e:
            db.session.rollback()
            print(f'❌ Error saving settings: {e}')
            return False
        
        print()
        print('📋 CURRENT CONFIGURATION:')
        print('   🌐 Server URL: http://localhost:8000 (when available)')
        print('   🔐 JWT Secret: ocr-agent-secret-key-2025')
        print('   📁 Storage URL: http://localhost:5000/storage')
        print('   🎛️ Mode: Local files (fallback)')
        print('   ⚡ Status: Disabled (until Document Server available)')
        print()
        print('💡 NEXT STEPS:')
        print('   1. OCR Agent will work without OnlyOffice integration')
        print('   2. Document editing will use download/upload workflow')
        print('   3. OnlyOffice can be enabled later when Document Server is available')
        print('   4. Test the settings panel: http://localhost:5000/panel/settings')
        
        return True

if __name__ == "__main__":
    configure_onlyoffice_settings()