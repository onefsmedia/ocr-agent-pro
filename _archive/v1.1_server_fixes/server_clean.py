#!/usr/bin/env python3
"""
OCR Agent Pro - Working Waitress Server
Clean implementation without Unicode issues
"""

import os
import sys
import time
import signal
from datetime import datetime

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"\nReceived signal {signum} - stopping server")
    sys.exit(0)

def check_dependencies():
    """Check if required packages are available"""
    try:
        from app import create_app
        print("Flask app: Available")
    except ImportError as e:
        print(f"Flask app error: {e}")
        return False
        
    try:
        from waitress import serve
        print("Waitress: Available")
    except ImportError:
        print("Waitress: Not installed")
        print("Install with: pip install waitress")
        return False
        
    return True

def test_database():
    """Test database connection"""
    try:
        from app import create_app
        from app.models import Document
        
        app = create_app()
        with app.app_context():
            doc_count = Document.query.count()
            print(f"Database connected: {doc_count} documents")
            return True
    except Exception as e:
        print(f"Database warning: {e}")
        return False

def start_server():
    """Start the Waitress server"""
    try:
        from app import create_app
        from waitress import serve
        
        print("Creating Flask app...")
        app = create_app()
        print("Flask app created successfully")
        
        # Test database
        test_database()
        
        print("Starting Waitress server...")
        print("URL: http://localhost:5000")
        print("Press Ctrl+C to stop")
        print("=" * 40)
        
        # Start server
        serve(app, host='0.0.0.0', port=5000, threads=6, channel_timeout=120)
        
    except Exception as e:
        print(f"Server error: {e}")
        raise

def main():
    """Main server function"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("OCR Agent Pro - Waitress Server")
    print("=" * 40)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not check_dependencies():
        print("Dependencies not satisfied")
        return False
    
    print("Starting server...")
    start_server()
    
    print("Server shutdown complete")
    return True

if __name__ == "__main__":
    main()