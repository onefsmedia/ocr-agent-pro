#!/usr/bin/env python3
"""
Direct Flask Server - Bypass Waitress Issues
"""

import os
import sys

# Set working directory
os.chdir(r'c:\OCR Agent')
sys.path.insert(0, r'c:\OCR Agent')

print("🚀 Starting OCR Agent Pro with Flask...")

try:
    from app import create_app
    app = create_app()
    print("✅ Flask app created")
    print("🌐 http://localhost:5000")
    print("🛑 Ctrl+C to stop")
    print()
    
    # Use Flask's built-in server with specific config
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
    
except KeyboardInterrupt:
    print("\n🛑 Stopped by user")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()