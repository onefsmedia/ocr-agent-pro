#!/usr/bin/env python3
"""
OnlyOffice Local Configuration Script for OCR Agent Pro
Configures local file handling mode while waiting for Document Server installation
"""

import os
import sys
import json
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import SystemSettings

def configure_onlyoffice_local():
    """Configure OnlyOffice for local file mode"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 CONFIGURING ONLYOFFICE LOCAL MODE")
        print("=" * 50)
        
        # OnlyOffice configuration settings
        settings_config = {
            # Basic OnlyOffice settings
            'onlyoffice_enabled': {
                'value': 'false',
                'description': 'Enable/disable OnlyOffice integration',
                'setting_type': 'boolean'
            },
            'onlyoffice_mode': {
                'value': 'local_files',
                'description': 'OnlyOffice operation mode (local_files, document_server)',
                'setting_type': 'string'
            },
            
            # Document Server settings (for future use)
            'onlyoffice_server_url': {
                'value': 'http://localhost:8000',
                'description': 'OnlyOffice Document Server URL',
                'setting_type': 'string'
            },
            'onlyoffice_jwt_secret': {
                'value': 'ocr-agent-secret-key-2025',
                'description': 'JWT secret for OnlyOffice authentication',
                'setting_type': 'string'
            },
            'onlyoffice_jwt_header': {
                'value': 'Authorization',
                'description': 'JWT header name for OnlyOffice',
                'setting_type': 'string'
            },
            'onlyoffice_jwt_in_body': {
                'value': 'true',
                'description': 'Include JWT in request body',
                'setting_type': 'boolean'
            },
            
            # Storage settings
            'onlyoffice_storage_path': {
                'value': os.path.join(os.path.dirname(__file__), 'storage', 'documents'),
                'description': 'Local storage path for OnlyOffice documents',
                'setting_type': 'string'
            },
            'onlyoffice_temp_path': {
                'value': os.path.join(os.path.dirname(__file__), 'storage', 'temp'),
                'description': 'Temporary storage path for OnlyOffice',
                'setting_type': 'string'
            },
            
            # API settings
            'onlyoffice_callback_url': {
                'value': 'http://localhost:5000/api/onlyoffice/callback',
                'description': 'Callback URL for OnlyOffice Document Server',
                'setting_type': 'string'
            },
            'onlyoffice_storage_url': {
                'value': 'http://localhost:5000/storage',
                'description': 'Storage URL for document access',
                'setting_type': 'string'
            },
            
            # File handling settings
            'onlyoffice_allowed_extensions': {
                'value': 'doc,docx,xls,xlsx,ppt,pptx,pdf,txt,rtf,odt,ods,odp',
                'description': 'Allowed file extensions for OnlyOffice editing',
                'setting_type': 'string'
            },
            'onlyoffice_max_file_size': {
                'value': '52428800',  # 50MB in bytes
                'description': 'Maximum file size for OnlyOffice editing (bytes)',
                'setting_type': 'integer'
            },
            
            # Editor settings
            'onlyoffice_document_type': {
                'value': 'word',
                'description': 'Default document type (word, cell, slide)',
                'setting_type': 'string'
            },
            'onlyoffice_lang': {
                'value': 'en',
                'description': 'Default language for OnlyOffice editor (en, fr)',
                'setting_type': 'string'
            }
        }
        
        # Create or update settings
        updated_count = 0
        created_count = 0
        
        for key, config in settings_config.items():
            existing_setting = SystemSettings.query.filter_by(key=key).first()
            
            if existing_setting:
                existing_setting.value = config['value']
                existing_setting.description = config['description']
                existing_setting.setting_type = config['setting_type']
                updated_count += 1
                print(f"✅ Updated: {key} = {config['value']}")
            else:
                setting = SystemSettings(
                    key=key,
                    value=config['value'],
                    description=config['description'],
                    setting_type=config['setting_type']
                )
                db.session.add(setting)
                created_count += 1
                print(f"🆕 Created: {key} = {config['value']}")
        
        # Create storage directories
        storage_path = settings_config['onlyoffice_storage_path']['value']
        temp_path = settings_config['onlyoffice_temp_path']['value']
        
        for path in [storage_path, temp_path]:
            os.makedirs(path, exist_ok=True)
            print(f"📁 Created directory: {path}")
        
        # Commit changes
        try:
            db.session.commit()
            print("\n✅ DATABASE CHANGES COMMITTED SUCCESSFULLY!")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR COMMITTING CHANGES: {e}")
            return False
        
        print(f"\n📊 CONFIGURATION SUMMARY:")
        print(f"   • Created: {created_count} new settings")
        print(f"   • Updated: {updated_count} existing settings")
        print(f"   • Total settings: {len(settings_config)}")
        
        print(f"\n🔧 ONLYOFFICE CONFIGURATION:")
        print(f"   • Mode: Local files (fallback mode)")
        print(f"   • Status: Disabled (waiting for Document Server)")
        print(f"   • Storage: {storage_path}")
        print(f"   • Temp: {temp_path}")
        print(f"   • Max file size: 50 MB")
        print(f"   • Supported formats: Office documents, PDF, text files")
        
        print(f"\n🚀 NEXT STEPS:")
        print(f"   1. Install OnlyOffice Document Server (download in progress)")
        print(f"   2. Update 'onlyoffice_enabled' setting to 'true'")
        print(f"   3. Change 'onlyoffice_mode' to 'document_server'")
        print(f"   4. Test document editing functionality")
        
        return True

def check_onlyoffice_installation():
    """Check if OnlyOffice components are installed"""
    
    print("\n🔍 CHECKING ONLYOFFICE INSTALLATION STATUS")
    print("=" * 50)
    
    # Check for Desktop Editors
    desktop_paths = [
        r"C:\Program Files\ONLYOFFICE\DesktopEditors",
        r"C:\Program Files (x86)\ONLYOFFICE\DesktopEditors",
        os.path.expanduser(r"~\AppData\Local\ONLYOFFICE")
    ]
    
    desktop_found = False
    for path in desktop_paths:
        if os.path.exists(path):
            print(f"✅ OnlyOffice Desktop Editors found: {path}")
            desktop_found = True
            break
    
    if not desktop_found:
        print("❌ OnlyOffice Desktop Editors not found")
    
    # Check for Document Server (future)
    print("❌ OnlyOffice Document Server: Installation pending")
    
    # Check downloaded installer
    installer_path = "onlyoffice-documentserver.exe"
    if os.path.exists(installer_path):
        size_mb = os.path.getsize(installer_path) / (1024 * 1024)
        print(f"📥 Document Server installer: {installer_path} ({size_mb:.1f} MB)")
    else:
        print("📥 Document Server installer: Download in progress")
    
    return desktop_found

def test_configuration():
    """Test the OnlyOffice configuration"""
    
    print("\n🧪 TESTING ONLYOFFICE CONFIGURATION")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test settings retrieval
            test_keys = ['onlyoffice_enabled', 'onlyoffice_mode', 'onlyoffice_storage_path']
            
            for key in test_keys:
                setting = SystemSettings.query.filter_by(key=key).first()
                if setting:
                    print(f"✅ {key}: {setting.value}")
                else:
                    print(f"❌ {key}: Not found")
            
            # Test storage directories
            storage_setting = SystemSettings.query.filter_by(key='onlyoffice_storage_path').first()
            temp_setting = SystemSettings.query.filter_by(key='onlyoffice_temp_path').first()
            
            if storage_setting and os.path.exists(storage_setting.value):
                print(f"✅ Storage directory accessible: {storage_setting.value}")
            else:
                print("❌ Storage directory not accessible")
                
            if temp_setting and os.path.exists(temp_setting.value):
                print(f"✅ Temp directory accessible: {temp_setting.value}")
            else:
                print("❌ Temp directory not accessible")
            
            print("\n✅ CONFIGURATION TEST COMPLETED!")
            return True
            
        except Exception as e:
            print(f"❌ Configuration test failed: {e}")
            return False

if __name__ == "__main__":
    print("🏢 ONLYOFFICE LOCAL CONFIGURATION SCRIPT")
    print("=" * 60)
    print("Setting up OCR Agent Pro for OnlyOffice integration...")
    print()
    
    try:
        # Step 1: Check current installation
        check_onlyoffice_installation()
        
        # Step 2: Configure local mode
        if configure_onlyoffice_local():
            print("\n✅ OnlyOffice local configuration completed successfully!")
            
            # Step 3: Test configuration
            test_configuration()
            
            print("\n🎉 ONLYOFFICE INTEGRATION READY!")
            print("=" * 60)
            print("The OCR Agent Pro system is now configured for OnlyOffice integration.")
            print("Currently running in local file mode as a fallback.")
            print("Document Server installation will upgrade to full functionality.")
            
        else:
            print("\n❌ Configuration failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)