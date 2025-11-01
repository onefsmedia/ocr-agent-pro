#!/usr/bin/env python3
"""
OnlyOffice Document Server Setup for OCR Agent Pro
"""

import os
import sys
import subprocess
import requests
import json
from pathlib import Path

def check_onlyoffice_running():
    """Check if OnlyOffice Document Server is running"""
    try:
        response = requests.get('http://localhost:8000/healthcheck', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def setup_onlyoffice_docker():
    """Setup OnlyOffice Document Server using Docker"""
    print("🐳 Setting up OnlyOffice Document Server with Docker...")
    
    # Create directories for OnlyOffice
    base_dir = Path('onlyoffice-data')
    directories = ['data', 'logs', 'cache', 'db']
    
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   Created directory: {dir_path}")
    
    # Docker command for OnlyOffice
    docker_cmd = [
        'docker', 'run', '-d',
        '--name', 'onlyoffice-documentserver',
        '-p', '8000:80',
        '--restart', 'unless-stopped',
        '-v', f'{base_dir.absolute() / "data"}:/var/www/onlyoffice/Data',
        '-v', f'{base_dir.absolute() / "logs"}:/var/log/onlyoffice',
        '-v', f'{base_dir.absolute() / "cache"}:/var/lib/onlyoffice/documentserver/App_Data/cache/files',
        '-v', f'{base_dir.absolute() / "db"}:/var/lib/postgresql',
        '-e', 'JWT_ENABLED=false',
        'onlyoffice/documentserver:latest'
    ]
    
    print("📦 Pulling and starting OnlyOffice Document Server...")
    print("   This may take a few minutes for the first time...")
    
    try:
        result = subprocess.run(docker_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ OnlyOffice Document Server started successfully!")
            print("🌐 OnlyOffice will be available at: http://localhost:8000")
            print("⏳ Please wait 30-60 seconds for the service to fully initialize...")
            return True
        else:
            print(f"❌ Failed to start OnlyOffice: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error starting OnlyOffice: {e}")
        return False

def setup_onlyoffice_native():
    """Instructions for native OnlyOffice installation"""
    print("🖥️  NATIVE ONLYOFFICE INSTALLATION")
    print("=" * 50)
    print()
    print("For Windows native installation:")
    print("1. Download OnlyOffice Document Server from:")
    print("   https://www.onlyoffice.com/download-docs.aspx")
    print()
    print("2. Install the .exe file")
    print()
    print("3. OnlyOffice will run on http://localhost")
    print("   Update OCR Agent settings to use port 80:")
    print("   Settings → OnlyOffice → Server URL: http://localhost")
    print()
    print("Alternative Docker Desktop method:")
    print("1. Install Docker Desktop for Windows")
    print("2. Run this script again to use Docker setup")
    print()

def create_onlyoffice_config():
    """Create OnlyOffice configuration in OCR Agent"""
    print("⚙️  Creating OnlyOffice configuration...")
    
    config = {
        'onlyoffice_url': 'http://localhost:8000',
        'onlyoffice_secret': 'ocr-agent-secret-2025',
        'onlyoffice_enabled': 'true',
        'onlyoffice_mode': 'server'
    }
    
    # Save to database if possible
    try:
        from app import create_app, db
        from app.models import SystemSettings
        
        app = create_app()
        with app.app_context():
            for key, value in config.items():
                setting = SystemSettings.query.filter_by(key=key).first()
                if setting:
                    setting.value = value
                else:
                    setting = SystemSettings(
                        key=key,
                        value=value,
                        description=f'OnlyOffice {key.replace("onlyoffice_", "").replace("_", " ").title()}',
                        setting_type='string'
                    )
                    db.session.add(setting)
            
            db.session.commit()
            print("✅ OnlyOffice configuration saved to database")
            
    except Exception as e:
        print(f"⚠️  Could not save to database: {e}")
        print("   You can configure OnlyOffice in OCR Agent settings manually")

def main():
    print("🏢 OCR AGENT PRO - ONLYOFFICE SETUP")
    print("=" * 50)
    print()
    
    # Check if OnlyOffice is already running
    if check_onlyoffice_running():
        print("✅ OnlyOffice Document Server is already running!")
        print("🌐 Available at: http://localhost:8000")
        print("📋 Admin panel: http://localhost:8000/welcome")
        create_onlyoffice_config()
        return
    
    print("🔍 OnlyOffice Document Server not detected...")
    print()
    
    # Check Docker availability
    if check_docker():
        print("✅ Docker detected")
        print()
        choice = input("🤔 Setup OnlyOffice with Docker? (y/n): ").lower().strip()
        
        if choice in ['y', 'yes']:
            if setup_onlyoffice_docker():
                create_onlyoffice_config()
                print()
                print("🎉 SETUP COMPLETE!")
                print()
                print("📋 NEXT STEPS:")
                print("1. Wait 30-60 seconds for OnlyOffice to initialize")
                print("2. Test connection: http://localhost:8000")
                print("3. Admin panel: http://localhost:8000/welcome")
                print("4. Restart OCR Agent Pro to apply settings")
            else:
                print("❌ Docker setup failed")
                setup_onlyoffice_native()
        else:
            setup_onlyoffice_native()
    else:
        print("❌ Docker not available")
        setup_onlyoffice_native()

if __name__ == '__main__':
    main()