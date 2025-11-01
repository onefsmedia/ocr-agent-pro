#!/usr/bin/env python3
"""
Ultra-Simple Waitress Server - No Background Threads
"""

import os
import sys

# Set working directory
os.chdir(r'c:\OCR Agent')
sys.path.insert(0, r'c:\OCR Agent')

print("🚀 Starting OCR Agent Pro...")

try:
    # Import app
    from app import create_app
    app = create_app()
    print("✅ Flask app created")
    
    # Import waitress  
    from waitress import serve
    print("✅ Waitress ready")
    
    print("🌐 http://localhost:5000")
    print("🛑 Ctrl+C to stop")
    print()
    
    # Simple serve - no threading complications
    serve(app, host='127.0.0.1', port=5000, threads=1)
    
except KeyboardInterrupt:
    print("\n🛑 Stopped by user")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()