#!/usr/bin/env python3
"""
Minimal diagnostic script to find the root cause
"""

import os
import sys
from pathlib import Path

# Set working directory and path
project_dir = Path(r'c:\OCR Agent')
os.chdir(project_dir)
sys.path.insert(0, str(project_dir))

def test_minimal_waitress():
    """Test Waitress with a minimal Flask app"""
    try:
        print("Step 1: Testing Waitress with minimal Flask app...")
        from flask import Flask
        from waitress import serve
        
        # Create minimal Flask app
        minimal_app = Flask(__name__)
        
        @minimal_app.route('/')
        def hello():
            return "Hello from minimal Flask app!"
        
        @minimal_app.route('/test')
        def test():
            return "Test endpoint working!"
        
        print("Step 2: Starting minimal Waitress server...")
        print("Server will run on http://localhost:5001")
        print("This tests if Waitress itself is working...")
        
        serve(minimal_app, host='127.0.0.1', port=5001, threads=2)
        
    except Exception as e:
        print(f"Minimal Waitress test failed: {e}")
        import traceback
        traceback.print_exc()

def test_ocr_app_creation():
    """Test OCR app creation without running server"""
    try:
        print("\nStep 3: Testing OCR app creation...")
        from app import create_app
        
        app = create_app()
        print("✅ OCR app created successfully")
        
        # Test if there are any issues with app configuration
        print(f"App name: {app.name}")
        print(f"Debug mode: {app.debug}")
        print(f"Testing mode: {app.testing}")
        
        # Test basic route
        with app.test_client() as client:
            response = client.get('/api/health')
            print(f"Health endpoint: {response.status_code}")
        
        print("✅ OCR app tested successfully - no issues found")
        return app
        
    except Exception as e:
        print(f"OCR app creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🔍 OCR Agent Pro - Diagnostic Script")
    print("=" * 50)
    
    # First test if the OCR app can be created
    ocr_app = test_ocr_app_creation()
    
    if ocr_app:
        print("\n✅ OCR app is fine - testing Waitress...")
        # Test minimal Waitress
        test_minimal_waitress()
    else:
        print("\n❌ OCR app has issues - fix app creation first")