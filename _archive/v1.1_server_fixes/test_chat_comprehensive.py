#!/usr/bin/env python3
"""
Comprehensive test for the chat API to isolate SQL issues
"""

import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
import requests
import time

def test_chat_with_full_app():
    """Test chat API with the full application setup"""
    
    print("🧪 Creating full Flask application...")
    
    try:
        app = create_app()
        
        print("✅ App created successfully")
        
        with app.app_context():
            # Test LLM service directly first
            print("🤖 Testing LLM service directly...")
            from app.services.llm_service import LLMService
            
            llm_service = LLMService()
            response = llm_service.generate_response("Hello", "", "You are a helpful assistant.")
            print(f"✅ LLM service working: {response[:50]}...")
            
            # Now test the route directly
            print("🌐 Testing chat route...")
            
            from app.routes.api import api_bp
            from flask import Flask
            
            # Create a minimal test app with just the API blueprint
            test_app = Flask(__name__)
            test_app.config.from_object('config.DevelopmentConfig')
            
            # Initialize database
            from app import db
            db.init_app(test_app)
            
            # Register only the API blueprint
            test_app.register_blueprint(api_bp, url_prefix='/api')
            
            with test_app.test_client() as client:
                print("📤 Sending test request...")
                
                response = client.post('/api/chat', 
                                     json={'message': 'Hello'},
                                     content_type='application/json')
                
                print(f"📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.get_json()
                    print(f"✅ Success: {data.get('response', 'No response')[:100]}...")
                else:
                    print(f"❌ Error: {response.get_data(as_text=True)}")
                    
                return response.status_code == 200
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chat_with_full_app()
    print("\n🏁 Test Result:", "✅ PASSED" if success else "❌ FAILED")