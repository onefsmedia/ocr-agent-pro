#!/usr/bin/env python3
"""
Test the chatbot panel to see what's different from dashboard
"""
import requests
import time

def test_chatbot_panel():
    """Test by accessing the chatbot panel page"""
    print("🧪 TESTING CHATBOT PANEL")
    print("=" * 50)
    
    try:
        # Test accessing the page
        response = requests.get('http://localhost:5000/panel/chatbot')
        print(f"📊 Page Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for key elements
            checks = {
                'chat-form': 'chat-form' in content,
                'message-input': 'message-input' in content,
                'chat-messages': 'chat-messages' in content,
                'sendMessage function': 'chat-form' in content and 'addEventListener' in content,
                'API endpoint': '/api/chat' in content,
                'Loading modal': 'loadingModal' in content
            }
            
            print("📋 Page Elements Check:")
            for element, found in checks.items():
                print(f"   {element}: {'✅' if found else '❌'}")
            
            # Test the API directly as the panel would
            print("\n🧪 Testing API as panel would call it...")
            api_response = requests.post(
                'http://localhost:5000/api/chat',
                json={'message': 'Hello from chatbot panel test', 'session_id': None},
                timeout=30
            )
            
            print(f"📊 API Status: {api_response.status_code}")
            if api_response.status_code == 200:
                data = api_response.json()
                print("✅ API Response Structure:")
                for key in ['response', 'session_id', 'context_used', 'timestamp']:
                    print(f"   {key}: {'✅' if key in data else '❌'}")
                print(f"🤖 Response: {data.get('response', 'No response')[:100]}...")
            else:
                print(f"❌ API failed: {api_response.text}")
                
        else:
            print(f"❌ Page failed to load: {response.text}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_chatbot_panel()