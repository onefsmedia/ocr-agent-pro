#!/usr/bin/env python3
"""
Test the scrollable chat sessions functionality
"""
import requests
import time

def test_scrollable_sessions():
    """Test that the chat sessions area is now scrollable"""
    print("🧪 TESTING SCROLLABLE CHAT SESSIONS")
    print("=" * 50)
    
    try:
        # Test accessing the chatbot panel page
        response = requests.get('http://localhost:5000/panel/chatbot')
        
        if response.status_code == 200:
            content = response.text
            
            # Check for the scrollable modifications
            checks = {
                'Fixed height': 'height: 400px' in content,
                'Overflow scroll': 'overflow-y: auto' in content,
                'Custom scrollbar CSS': 'webkit-scrollbar' in content,
                'Session hover effects': 'session-item:hover' in content,
                'Scrollbar styling': 'scrollbar-width: thin' in content
            }
            
            print("📋 Scrollable Features Check:")
            for feature, found in checks.items():
                status = "✅" if found else "❌"
                print(f"   {feature}: {status}")
            
            if all(checks.values()):
                print("\n✅ All scrollable features implemented correctly!")
                print("📊 Chat sessions area details:")
                print("   - Fixed height: 400px")
                print("   - Overflow: auto (scrollable)")
                print("   - Custom scrollbar styling")
                print("   - Enhanced hover effects")
                print("   - Session separators")
                return True
            else:
                print("\n❌ Some features missing!")
                return False
                
        else:
            print(f"❌ Failed to load page: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def create_test_sessions():
    """Create a few test chat sessions to verify scrolling"""
    print("\n🧪 CREATING TEST SESSIONS FOR SCROLLING")
    print("=" * 50)
    
    test_messages = [
        "Hello, this is test session 1",
        "This is test session 2 with a longer message",
        "Test session 3 - checking scrollability",
        "Another test session for scroll verification",
        "Session 5 - making sure we have enough to scroll",
        "Session 6 - more content for scrolling test",
        "Session 7 - final test session"
    ]
    
    successful_sessions = 0
    
    for i, message in enumerate(test_messages, 1):
        try:
            response = requests.post(
                'http://localhost:5000/api/chat',
                json={'message': message, 'session_id': None},
                timeout=30
            )
            
            if response.status_code == 200:
                successful_sessions += 1
                print(f"   ✅ Session {i} created")
            else:
                print(f"   ❌ Session {i} failed")
                
        except Exception as e:
            print(f"   ❌ Session {i} error: {e}")
            
        # Small delay between requests
        time.sleep(0.5)
    
    print(f"\n📊 Created {successful_sessions}/{len(test_messages)} test sessions")
    print("💡 Now visit the chatbot panel to see the scrollable sessions!")
    
    return successful_sessions > 0

if __name__ == "__main__":
    # Test the scrollable implementation
    scrollable_success = test_scrollable_sessions()
    
    # Create test sessions if the scrollable implementation is working
    if scrollable_success:
        sessions_success = create_test_sessions()
    else:
        sessions_success = False
    
    print("\n" + "=" * 50)
    print("🏁 TEST SUMMARY:")
    print(f"   Scrollable Implementation: {'✅ SUCCESS' if scrollable_success else '❌ FAILED'}")
    print(f"   Test Sessions Created: {'✅ SUCCESS' if sessions_success else '❌ FAILED'}")
    
    if scrollable_success and sessions_success:
        print("\n🎉 SCROLLABLE CHAT SESSIONS READY!")
        print("🌐 Visit: http://localhost:5000/panel/chatbot")
        print("📋 Features:")
        print("   - Sessions list limited to 400px height")
        print("   - Automatic scrolling when sessions exceed height")
        print("   - Custom styled scrollbar")
        print("   - Enhanced hover effects")
        print("   - Page no longer extends with more sessions")