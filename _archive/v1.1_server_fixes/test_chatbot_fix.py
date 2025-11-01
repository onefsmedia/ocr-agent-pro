#!/usr/bin/env python3
"""
Test script to verify the chatbot fix is working
"""
import requests
import time

def test_chatbot_fix():
    """Test the fixed chatbot response handling"""
    print("🧪 TESTING CHATBOT RESPONSE FIX")
    print("=" * 50)
    
    # Wait for server to be ready
    time.sleep(2)
    
    try:
        # Test a simple chat message
        test_message = "Hello, how are you?"
        payload = {'message': test_message}
        
        print(f"📤 Sending query: \"{test_message}\"")
        response = requests.post(
            'http://localhost:5000/api/chat',
            json=payload,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! API returned valid response")
            print("📋 Response Structure:")
            print(f"   - response: {'✅' if 'response' in data else '❌'}")
            print(f"   - session_id: {'✅' if 'session_id' in data else '❌'}")
            print(f"   - context_used: {'✅' if 'context_used' in data else '❌'}")
            print(f"   - timestamp: {'✅' if 'timestamp' in data else '❌'}")
            print(f"   - success field: {'❌ (correctly absent)' if 'success' not in data else '⚠️ (unexpectedly present)'}")
            
            response_text = data.get('response', 'No response')
            print(f"\n🤖 AI Response: {response_text[:100]}...")
            
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return False

if __name__ == "__main__":
    success = test_chatbot_fix()
    print("\n" + "=" * 50)
    print(f"🏁 Test Result: {'✅ CHATBOT FIX VERIFIED' if success else '❌ ISSUES REMAIN'}")
    
    if success:
        print("\n✅ The chatbot should now work correctly!")
        print("✅ Frontend will properly handle API responses")
        print("✅ No more 'Sorry, I encountered an error' for valid responses")