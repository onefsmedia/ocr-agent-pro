#!/usr/bin/env python3
"""
Debug script to isolate the chat API SQL error
"""

import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
import traceback

def debug_chat():
    """Test the chat function step by step"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔍 Testing minimal chat functionality...")
            
            # Import only what we need
            from app.services.llm_service import LLMService
            
            print("✅ Imports successful")
            
            # Test LLM service directly
            print("🤖 Testing LLM service...")
            llm_service = LLMService()
            print(f"✅ LLM service initialized: {llm_service.provider}")
            
            # Test simple response
            response = llm_service.generate_response("Hello")
            print(f"✅ LLM response: {response[:100]}...")
            
            print("🎉 All tests passed!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    debug_chat()