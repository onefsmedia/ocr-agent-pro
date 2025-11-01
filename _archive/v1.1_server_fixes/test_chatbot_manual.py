#!/usr/bin/env python3
"""
Simple test to check what happens in the chatbot panel
"""
import requests
import time

def manual_test_chatbot_panel():
    """Manual test to debug the chatbot panel issue"""
    print("🧪 MANUAL CHATBOT PANEL DEBUG")
    print("=" * 50)
    
    print("1. Testing API endpoint directly...")
    try:
        response = requests.post(
            'http://localhost:5000/api/chat',
            json={
                'message': 'Hello from manual test',
                'session_id': None
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response Structure:")
            for key, value in data.items():
                if key == 'response':
                    print(f"   {key}: {str(value)[:100]}...")
                else:
                    print(f"   {key}: {value}")
            print()
        else:
            print(f"❌ API failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API error: {e}")
        return False
    
    print("2. Testing page accessibility...")
    try:
        page_response = requests.get('http://localhost:5000/panel/chatbot')
        if page_response.status_code == 200:
            print("✅ Chatbot panel page loads correctly")
            
            # Check for key elements in the HTML
            content = page_response.text
            checks = {
                'chat-form': 'id="chat-form"' in content,
                'message-input': 'id="message-input"' in content,
                'chat-messages': 'id="chat-messages"' in content,
                'loadingModal': 'id="loadingModal"' in content,
                'JavaScript block': '<script>' in content and 'addEventListener' in content,
                'Bootstrap modal': 'bootstrap.Modal' in content,
                'API endpoint': '/api/chat' in content
            }
            
            print("📋 Page Element Checks:")
            for element, found in checks.items():
                status = "✅" if found else "❌"
                print(f"   {element}: {status}")
                
            if not all(checks.values()):
                print("\n❌ Some elements are missing!")
                return False
            else:
                print("\n✅ All required elements found in HTML")
                
        else:
            print(f"❌ Page failed to load: {page_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Page test error: {e}")
        return False
    
    print("\n3. Comparison with dashboard quick chat...")
    try:
        dashboard_response = requests.get('http://localhost:5000/')
        if dashboard_response.status_code == 200:
            dashboard_content = dashboard_response.text
            
            # Check what the dashboard uses
            dashboard_checks = {
                'quickChat function': 'function quickChat()' in dashboard_content,
                'quick-chat-input': 'id="quick-chat-input"' in dashboard_content,
                'quick-chat-response': 'id="quick-chat-response"' in dashboard_content,
                'API call': '/api/chat' in dashboard_content
            }
            
            print("📋 Dashboard Chat Elements:")
            for element, found in dashboard_checks.items():
                status = "✅" if found else "❌"
                print(f"   {element}: {status}")
                
        else:
            print("❌ Dashboard failed to load")
            
    except Exception as e:
        print(f"❌ Dashboard test error: {e}")
    
    print("\n💡 DIAGNOSIS:")
    print("If the API works and the page loads correctly,")
    print("the issue is likely in the JavaScript execution.")
    print("\nPossible causes:")
    print("- Loading modal not hiding properly")
    print("- JavaScript errors in browser console")
    print("- CSS preventing messages from showing")
    print("- Session ID handling issues")
    
    return True

if __name__ == "__main__":
    success = manual_test_chatbot_panel()
    print("\n" + "=" * 50)
    print(f"🏁 Test Result: {'✅ DIAGNOSTIC COMPLETE' if success else '❌ ISSUES FOUND'}")
    
    if success:
        print("\n🔧 NEXT STEPS:")
        print("1. Open browser developer tools")
        print("2. Go to http://localhost:5000/panel/chatbot")
        print("3. Check Console tab for JavaScript errors")
        print("4. Try sending a message and watch the Network tab")
        print("5. Check if the loading modal is hiding properly")