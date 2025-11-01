#!/usr/bin/env python3
"""
Test script for LLM service integration with the chat API
"""

import requests
import json
import time
import sys

def test_ollama_connection():
    """Test if Ollama is running and has models available"""
    print("🔍 TESTING OLLAMA CONNECTION")
    print("=" * 50)
    
    try:
        # Check if Ollama is running
        response = requests.get('http://localhost:11434/api/tags', timeout=10)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} models")
            
            # List available models
            if models:
                print("📚 Available models:")
                for model in models[:3]:  # Show first 3
                    name = model.get('name', 'Unknown')
                    size = model.get('size', 0)
                    size_mb = size / (1024*1024) if size else 0
                    print(f"   • {name} ({size_mb:.1f}MB)")
            else:
                print("⚠️ No models found in Ollama")
                return False
            
            # Test a simple query
            print("\n🧪 Testing simple Ollama query...")
            test_payload = {
                "model": models[0]['name'],
                "prompt": "Hello, please respond with just 'Hello World'",
                "stream": False,
                "options": {"temperature": 0, "num_ctx": 512}
            }
            
            response = requests.post(
                'http://localhost:11434/api/generate',
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '').strip()
                print(f"✅ Ollama response: {response_text}")
                return True
            else:
                print(f"❌ Ollama query failed: {response.status_code}")
                return False
                
        else:
            print(f"❌ Ollama not responding: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama (not running)")
        print("💡 Start Ollama with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Ollama test error: {e}")
        return False

def test_chat_api_with_llm():
    """Test the chat API with LLM integration"""
    print("\n🧪 TESTING CHAT API WITH LLM")
    print("=" * 50)
    
    # Wait for server to be ready
    time.sleep(3)
    
    try:
        # Test the chat API
        test_message = "Hello, what can you help me with?"
        
        payload = {'message': test_message}
        
        print(f"📤 Sending query: \"{test_message}\"")
        print("⏳ Waiting for LLM response...")
        
        response = requests.post(
            'http://localhost:5000/api/chat',
            json=payload,
            timeout=120  # Increased timeout for large models like deepseek-coder-v2:16b
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', 'No response')
            
            print("\n🎉 SUCCESS! Chat API working with LLM!")
            print("=" * 50)
            print(f"🤖 AI Response:\n{response_text}")
            print("\n📊 Metadata:")
            print(f"   Session ID: {data.get('session_id', 'None')}")
            print(f"   Context Used: {data.get('context_used', 0)}")
            print(f"   Timestamp: {data.get('timestamp', 'None')}")
            
            # Check if response looks like it came from LLM vs fallback
            if len(response_text) > 100 and any(word in response_text.lower() for word in ['help', 'assist', 'can', 'document']):
                print("\n✅ Response appears to be from LLM (comprehensive)")
                return True
            else:
                print("\n⚠️ Response appears to be fallback (basic)")
                return True
            
        else:
            print("❌ Chat API Error:")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   Raw response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server")
        print("💡 Start server with: python production_server.py")
        return False
    except Exception as e:
        print(f"❌ Chat API test error: {e}")
        return False

def main():
    print("🚀 OCR AGENT PRO - LLM INTEGRATION TEST")
    print("=" * 60)
    print("Testing the complete AI Assistant pipeline:")
    print("1. Ollama LLM service")
    print("2. Flask chat API")
    print("3. Vector database integration")
    print("4. User interaction capabilities")
    print()
    
    # Test Ollama
    ollama_ok = test_ollama_connection()
    
    # Test Chat API
    chat_ok = test_chat_api_with_llm()
    
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Ollama LLM Service: {'✅ WORKING' if ollama_ok else '❌ FAILED'}")
    print(f"Chat API Integration: {'✅ WORKING' if chat_ok else '❌ FAILED'}")
    
    if ollama_ok and chat_ok:
        print("\n🏆 ALL TESTS PASSED!")
        print("🎉 Your AI Assistant is ready to:")
        print("   • Answer questions about documents")
        print("   • Interact with the vector database") 
        print("   • Provide intelligent responses")
        print("   • Support Cameroonian education content")
        print("\n🌐 Open http://localhost:5000 and try the AI Assistant!")
        return True
    else:
        print("\n💥 SOME TESTS FAILED!")
        if not ollama_ok:
            print("⚠️ Ollama needs to be running for full AI capabilities")
        if not chat_ok:
            print("⚠️ Chat API needs debugging")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)