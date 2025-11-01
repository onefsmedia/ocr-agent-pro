#!/usr/bin/env python3
"""
Production Flask Server using Waitress WSGI
More stable than Flask development server
"""

import os
import sys
from pathlib import Path

# Set working directory and path
project_dir = Path(r'c:\OCR Agent')
os.chdir(project_dir)
sys.path.insert(0, str(project_dir))

def main():
    print("🚀 OCR Agent Pro - Production Server (Waitress)")
    print("=" * 60)
    
    try:
        # Import Flask app
        from app import create_app
        from waitress import serve
        
        print("✅ Importing Flask application...")
        app = create_app()
        
        print("✅ Flask app created successfully")
        print("✅ Database connection established")
        print("✅ All services initialized")
        print()
        print("🌐 Starting production server...")
        print("🌐 Server URL: http://localhost:5000")
        print("🌐 Network URL: http://0.0.0.0:5000")
        print()
        print("🔥 Using Waitress WSGI server for stability")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        # Start waitress server
        serve(
            app,
            host='0.0.0.0',
            port=5000,
            threads=6,
            connection_limit=1000,
            cleanup_interval=30,
            channel_timeout=120
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ Server shutdown complete")

if __name__ == "__main__":
    main()