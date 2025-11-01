#!/usr/bin/env python3
"""
Test the chatbot panel by sending a request via JavaScript simulation
"""
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def test_chatbot_panel_ui():
    """Test the chatbot panel UI directly"""
    print("🧪 TESTING CHATBOT PANEL UI")
    print("=" * 50)
    
    # Check if we can use selenium (might not be installed)
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Try to start the browser with automatic driver management
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            # Navigate to the chatbot panel
            driver.get("http://localhost:5000/panel/chatbot")
            print("✅ Page loaded successfully")
            
            # Wait for the form to be present
            wait = WebDriverWait(driver, 10)
            chat_form = wait.until(EC.presence_of_element_located((By.ID, "chat-form")))
            message_input = driver.find_element(By.ID, "message-input")
            
            print("✅ Found chat form and input")
            
            # Type a message
            message_input.send_keys("Hello, this is a test message")
            print("✅ Message typed")
            
            # Submit the form
            chat_form.submit()
            print("✅ Form submitted")
            
            # Wait for response (look for new messages)
            time.sleep(5)
            
            # Check for any JavaScript errors in console
            logs = driver.get_log('browser')
            if logs:
                print("🚨 JavaScript Console Errors:")
                for log in logs:
                    print(f"   {log['level']}: {log['message']}")
            else:
                print("✅ No JavaScript errors found")
            
            # Check if messages were added
            chat_messages = driver.find_element(By.ID, "chat-messages")
            message_elements = chat_messages.find_elements(By.CLASS_NAME, "chat-message")
            
            print(f"📊 Found {len(message_elements)} chat messages")
            
            if len(message_elements) > 0:
                print("✅ Messages were added to the chat")
                for i, msg in enumerate(message_elements):
                    print(f"   Message {i+1}: {msg.text[:50]}...")
            else:
                print("❌ No messages found - this indicates the issue")
                # Print the current HTML to debug
                print("📋 Current chat-messages content:")
                print(chat_messages.get_attribute('innerHTML')[:500])
            
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"❌ Selenium test failed: {e}")
        print("💡 This might be due to missing ChromeDriver or Selenium not installed")
        return False
        
    return True

def test_simple_api():
    """Simple API test as fallback"""
    print("\n🧪 FALLBACK: SIMPLE API TEST")
    print("=" * 30)
    
    try:
        response = requests.post(
            'http://localhost:5000/api/chat',
            json={'message': 'Test message', 'session_id': None},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API works correctly")
            print(f"🤖 Response: {data.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"❌ API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    # First try selenium test, then fallback to simple API test
    ui_success = test_chatbot_panel_ui()
    api_success = test_simple_api()
    
    print("\n" + "=" * 50)
    print("🏁 TEST SUMMARY:")
    print(f"   UI Test: {'✅ PASSED' if ui_success else '❌ FAILED/SKIPPED'}")
    print(f"   API Test: {'✅ PASSED' if api_success else '❌ FAILED'}")
    
    if not ui_success and api_success:
        print("\n💡 The API works but the UI might have issues.")
        print("   This suggests a frontend JavaScript problem.")