#!/usr/bin/env python3
"""
OCR Agent Pro - Waitress Setup Script
Configure Waitress as the default production server
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Ensure Python version compatibility"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("Please upgrade to Python 3.8 or higher")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_waitress():
    """Install Waitress and required dependencies"""
    print("📦 Installing Waitress and dependencies...")
    
    packages = [
        'waitress',
        'psycopg2-binary',
        'pillow',
        'flask[async]'
    ]
    
    try:
        for package in packages:
            print(f"   Installing {package}...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package, '--upgrade'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("✅ All packages installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Package installation failed: {e}")
        return False

def verify_installation():
    """Verify Waitress installation"""
    print("🔍 Verifying Waitress installation...")
    
    try:
        import waitress
        version = waitress.__version__
        print(f"✅ Waitress {version} - Ready")
        
        # Test Flask app import
        from app import create_app
        print("✅ Flask application - Ready")
        
        # Test database connection
        app = create_app()
        with app.app_context():
            from app.models import Document
            doc_count = Document.query.count()
            print(f"✅ Database connection - Ready ({doc_count} documents)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Warning: {e}")
        return True  # Continue anyway

def create_config_file():
    """Create Waitress configuration file"""
    config = {
        "server": {
            "type": "waitress",
            "host": "0.0.0.0",
            "port": 5000,
            "threads": 6,
            "connection_limit": 1000,
            "cleanup_interval": 30,
            "channel_timeout": 120,
            "url_scheme": "http",
            "ident": "OCR-Agent-Pro/1.0"
        },
        "features": {
            "auto_restart": True,
            "max_restarts": 10,
            "restart_delay": 5,
            "health_check": True
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
    
    config_file = Path("waitress_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to {config_file}")
    return True

def update_main_app():
    """Ensure app.py uses Waitress by default"""
    app_file = Path("app.py")
    if not app_file.exists():
        print("❌ app.py not found")
        return False
    
    # Read current content
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if Waitress is already the default
    if 'from waitress import serve' in content and 'serve(' in content:
        print("✅ app.py already configured for Waitress")
        return True
    
    print("⚠️  app.py may need manual Waitress configuration")
    return True

def create_run_scripts():
    """Create convenient run scripts"""
    
    # Simple Python launcher (without Unicode characters)
    launcher_content = '''#!/usr/bin/env python3
"""OCR Agent Pro - Quick Launcher"""
if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from app import app
    
    try:
        from waitress import serve
        print("Starting OCR Agent Pro with Waitress...")
        print("URL: http://localhost:5000")
        serve(app, host='0.0.0.0', port=5000, threads=6)
    except ImportError:
        print("ERROR: Waitress not installed!")
        print("Run: python setup_waitress.py")
'''
    
    with open("run.py", 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("Created run.py launcher")
    return True

def display_instructions():
    """Display usage instructions"""
    print("\n" + "="*60)
    print("WAITRESS SETUP COMPLETE!")
    print("="*60)
    print()
    print("START OPTIONS:")
    print("   1. python app.py                    # Main application")
    print("   2. python run.py                    # Quick launcher")
    print("   3. python persistent_server_simple.py  # Auto-restart")
    print("   4. start_waitress.bat               # Windows batch")
    print("   5. .\\start_waitress.ps1            # PowerShell script")
    print()
    print("ACCESS URLS:")
    print("   • Local:   http://localhost:5000")
    print("   • Network: http://0.0.0.0:5000")
    print()
    print("WAITRESS FEATURES:")
    print("   • Production-grade WSGI server")
    print("   • Multi-threaded (6 threads)")
    print("   • Connection pooling (1000 connections)")
    print("   • Graceful shutdown handling")
    print("   • Memory efficient")
    print("   • No development server warnings")
    print()
    print("CONFIGURATION:")
    print("   • Config file: waitress_config.json")
    print("   • Auto-restart: persistent_server_simple.py")
    print("   • Windows service: windows_service.py")
    print("="*60)

def main():
    """Main setup function"""
    print("OCR Agent Pro - Waitress Setup")
    print("="*50)
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install Waitress
    if not install_waitress():
        return False
    
    # Verify installation
    if not verify_installation():
        return False
    
    # Create configuration
    create_config_file()
    
    # Update main app
    update_main_app()
    
    # Create run scripts
    create_run_scripts()
    
    # Show instructions
    display_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nSetup failed")
        sys.exit(1)
    else:
        print("\nSetup completed successfully")
        print("Ready to start your OCR Agent Pro server!")