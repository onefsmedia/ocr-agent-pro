#!/usr/bin/env python3
"""
Simple test script for direct Flask chat API testing
"""

import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
import requests
import json

def test_simple_chat():
    """Test the chat API with a direct HTTP request"""
    
    app = create_app()
    
    # Start the test server
    import threading
    from werkzeug.serving import make_server
    
    server = make_server('127.0.0.1', 5001, app)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    import time
    time.sleep(1)  # Give server time to start
    
    try:
        print("🧪 Testing direct chat API...")
        
        # Test simple chat
        response = requests.post(
            "http://127.0.0.1:5001/api/chat",
            json={"message": "Hello"},
            timeout=60
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat Response: {data.get('response', 'No response')[:100]}...")
            print("🎉 Chat API working!")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        server.shutdown()

if __name__ == "__main__":
    test_simple_chat()