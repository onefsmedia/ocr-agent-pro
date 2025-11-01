#!/usr/bin/env python3
"""
Minimal server for troubleshooting
"""

import os
import sys
from pathlib import Path

# Set working directory and path
project_dir = Path(r'c:\OCR Agent')
os.chdir(project_dir)
sys.path.insert(0, str(project_dir))

def test_app_creation():
    """Test if the app can be created without issues"""
    try:
        print("Testing app creation...")
        from app import create_app
        
        app = create_app()
        print("✅ App created successfully")
        
        # Test a simple route
        with app.test_client() as client:
            response = client.get('/')
            print(f"✅ Dashboard route test: HTTP {response.status_code}")
            
        return app
        
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("🔧 OCR Agent Pro - Troubleshooting Server")
    print("=" * 50)
    
    app = test_app_creation()
    if not app:
        return 1
    
    print()
    print("🌐 Starting server with minimal configuration...")
    
    try:
        # Try Waitress first
        from waitress import serve
        print("✅ Waitress available, starting production server...")
        print("🌐 Server URL: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)
        
        serve(app, host='127.0.0.1', port=5000, threads=4)
        
    except ImportError:
        print("⚠️ Waitress not available, using Flask dev server...")
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("✅ Server shutdown complete")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)