#!/usr/bin/env python3
"""
OCR Agent Pro - Final Working Server
Simplified approach that actually stays running
"""

import os
import sys

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the server the simple way"""
    try:
        print("OCR Agent Pro - Starting Server")
        print("=" * 40)
        
        # Import everything we need
        from app import create_app
        from waitress import serve
        
        # Create the Flask app
        app = create_app()
        print("✓ Flask app created")
        
        # Test database
        with app.app_context():
            from app.models import Document
            doc_count = Document.query.count()
            print(f"✓ Database: {doc_count} documents")
        
        print()
        print("🌐 Server starting on http://localhost:5000")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 40)
        
        # Start Waitress - this will block until interrupted
        serve(app, host='0.0.0.0', port=5000, threads=6)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)