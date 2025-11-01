#!/usr/bin/env python3
"""
Quick Waitress Server - Immediate Fix
"""

import os
import sys

# Simple setup
os.chdir(r'c:\OCR Agent')
sys.path.insert(0, r'c:\OCR Agent')

print("🚀 Quick Server Starting...")

try:
    from app import create_app
    from waitress import serve
    
    app = create_app()
    print("✅ App ready")
    print("🌐 Server on http://localhost:5000")
    
    serve(app, host='0.0.0.0', port=5000)
    
except Exception as e:
    print(f"❌ Error: {e}")