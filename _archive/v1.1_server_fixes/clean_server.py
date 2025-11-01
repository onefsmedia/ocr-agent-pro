#!/usr/bin/env python3
"""
OCR Agent Pro - Clean Production Server
No signal handling complications
"""

import os
import sys

def main():
    """Clean server startup"""
    # Set working directory
    project_dir = r'c:\OCR Agent'
    os.chdir(project_dir)
    sys.path.insert(0, project_dir)
    
    print("OCR Agent Pro - Clean Production Server")
    print("======================================")
    
    try:
        # Import and create app
        from app import create_app
        app = create_app()
        print("✅ Flask application created")
        
        # Start server with minimal configuration
        print("🌐 Server starting on http://localhost:5000")
        print("🛑 Press Ctrl+C to stop")
        print()
        
        # Simple Flask server without signal complications
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            use_debugger=False,
            passthrough_errors=False,
            threaded=True
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()