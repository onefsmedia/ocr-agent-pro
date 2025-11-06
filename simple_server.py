#!/usr/bin/env python3
"""
Simple server for testing prompt functionality
"""
from app import create_app
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*60)
    print("🚀 Starting OCR Agent Debug Server")
    print("="*60)
    print("URL: http://localhost:5002")
    print("Settings: http://localhost:5002/panel/settings#prompts")
    print("="*60)
    
    try:
        app.run(host='127.0.0.1', port=5002, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        import traceback
        traceback.print_exc()