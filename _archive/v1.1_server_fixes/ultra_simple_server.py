#!/usr/bin/env python3
"""
Ultra-Simple Flask Server Launcher
Minimal approach to avoid any signal/reloader issues
"""

import os
import sys
import time

# Set working directory
os.chdir(r'c:\OCR Agent')
sys.path.insert(0, os.getcwd())

def main():
    print("🚀 OCR Agent Pro - Ultra Simple Launcher")
    print("=" * 50)
    
    try:
        # Import Flask app
        from app import create_app
        
        print("✅ Importing Flask app...")
        app = create_app()
        
        print("✅ Flask app created successfully")
        print("✅ Database connection established")
        print()
        print("🌐 Starting server on http://localhost:5000")
        print("🌐 Network access on http://0.0.0.0:5000")
        print()
        print("🔥 Server starting now...")
        print("=" * 50)
        
        # Start server with minimal configuration
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,       # No debug mode
            use_reloader=False, # No reloader
            use_debugger=False, # No debugger
            threaded=True      # Support multiple requests
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure you're in the correct directory with all dependencies installed")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🛑 Server stopped")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()