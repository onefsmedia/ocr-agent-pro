#!/usr/bin/env python3
"""
Background Flask Server for OCR Agent Pro
Starts server in background and keeps it running
"""

import os
import sys
import threading
import time
import signal
from pathlib import Path

# Set working directory
os.chdir(r'c:\OCR Agent')
sys.path.insert(0, os.getcwd())

def run_flask_server():
    """Run Flask server in background thread"""
    try:
        from app import create_app
        app = create_app()
        
        print("✅ Flask app initialized")
        print("✅ Database connected")
        
        # Run server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            use_debugger=False,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🚀 OCR Agent Pro - Background Server")
    print("=" * 50)
    
    # Start server in daemon thread
    server_thread = threading.Thread(target=run_flask_server, daemon=True)
    server_thread.start()
    
    print("✅ Server thread started")
    print("⏳ Waiting for server initialization...")
    
    # Wait for server to start
    time.sleep(3)
    
    print()
    print("🌐 OCR Agent Pro is now running!")
    print("🌐 Access at: http://localhost:5000")
    print("🌐 Network access: http://0.0.0.0:5000")
    print()
    print("🔄 Server running in background...")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        print("✅ Server stopped")

if __name__ == "__main__":
    main()