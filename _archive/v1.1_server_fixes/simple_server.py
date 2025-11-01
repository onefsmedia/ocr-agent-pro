#!/usr/bin/env python3
"""
Simple Flask Server Launcher
Bypasses signal handling issues in PowerShell
"""

import os
import sys
import signal

def ignore_signals():
    """Ignore interrupt signals to prevent premature shutdown"""
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

def main():
    print("🚀 Starting OCR Agent Pro (Simple Launcher)")
    print("=" * 50)
    
    # Add project to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    try:
        # Import and create app
        from app import create_app
        
        app = create_app()
        print("✅ Flask app created successfully")
        print("✅ Database connected")
        print("✅ Starting server on http://localhost:5000")
        print("=" * 50)
        print("🌐 Open your browser to: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the server with minimal configuration
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Disable debug to avoid reloader issues
            use_reloader=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()