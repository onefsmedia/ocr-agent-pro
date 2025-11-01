#!/usr/bin/env python3
"""
OCR Agent Pro - Production Server
Stable deployment without Unicode logging issues
"""

import os
import sys
import signal

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("Server shutting down gracefully...")
    sys.exit(0)

def main():
    """Production server startup"""
    # Set working directory
    project_dir = r'c:\OCR Agent'
    os.chdir(project_dir)
    sys.path.insert(0, project_dir)
    
    print("OCR Agent Pro - Production Server")
    print("==================================")
    print(f"Working Directory: {project_dir}")
    
    try:
        # Create Flask application
        print("Creating Flask application...")
        from app import create_app
        app = create_app()
        print("Flask app created successfully")
        
        # Start production server
        print("Starting server on http://localhost:5000")
        print("Press Ctrl+C to stop")
        print("")
        
        # Use Flask with production-like settings
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    main()