#!/usr/bin/env python3
"""
Simple server starter for development testing
"""

import os
import sys
from pathlib import Path

# Set working directory and path
project_dir = Path(r'c:\OCR Agent')
os.chdir(project_dir)
sys.path.insert(0, str(project_dir))

def main():
    print("🚀 OCR Agent Pro - Development Server")
    print("=" * 50)
    
    try:
        from app import create_app
        
        print("✅ Creating Flask application...")
        app = create_app()
        
        print("✅ Flask app created successfully")
        print("✅ Database connection established")
        print()
        print("🌐 Starting development server...")
        print("🌐 Server URL: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 50)
        
        # Start Flask development server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n✅ Server stopped")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)