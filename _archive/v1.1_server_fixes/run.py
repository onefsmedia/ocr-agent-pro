#!/usr/bin/env python3
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
