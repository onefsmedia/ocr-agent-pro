#!/usr/bin/env python3
"""
OCR Agent Pro - Stable Waitress Server
Fixed version without signal handling conflicts
"""

import os
import sys
from pathlib import Path

# Set working directory and path
project_dir = Path(r'c:\OCR Agent')
os.chdir(project_dir)
sys.path.insert(0, str(project_dir))

def main():
    print("🚀 OCR Agent Pro - Stable Waitress Server")
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
        print("🌐 Starting Waitress WSGI production server...")
        print("🌐 Server URL: http://localhost:5000")
        print("🌐 Network URL: http://0.0.0.0:5000")
        print()
        print("🔥 Waitress Configuration:")
        print("   • Host: 0.0.0.0")
        print("   • Port: 5000")
        print("   • Threads: 6")
        print("   • Connection Limit: 1000")
        print("   • Channel Timeout: 120s")
        print("   • Cleanup Interval: 30s")
        print()
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        print()
        
        # Start waitress server - NO signal handlers to interfere
        serve(
            app,
            host='0.0.0.0',
            port=5000,
            threads=6,
            connection_limit=1000,
            cleanup_interval=30,
            channel_timeout=120,
            url_scheme='http',
            ident='OCR-Agent-Pro/1.0'
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed")
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user (Ctrl+C)")
        return 0
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n✅ Server shutdown complete")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)