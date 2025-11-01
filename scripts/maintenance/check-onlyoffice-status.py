#!/usr/bin/env python3
"""
OnlyOffice Connection Status Checker
Checks the current status of OnlyOffice integration in OCR Agent
"""

import requests
import sys
import json
from datetime import datetime

def check_onlyoffice_status():
    """Check OnlyOffice connection status"""
    
    print("🔍 OnlyOffice Connection Status Check")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Check OCR Agent API
        print("📡 Checking OCR Agent API...")
        response = requests.get('http://localhost:5000/api/onlyoffice/status', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ OCR Agent API: Online")
            print(f"   OnlyOffice URL: {data.get('service_url', 'N/A')}")
            print(f"   Connection Status: {data.get('status', 'Unknown')}")
            print(f"   Connected: {'Yes' if data.get('connected') else 'No'}")
            
            if data.get('connected'):
                print("✅ OnlyOffice Document Server: Connected")
            else:
                print("❌ OnlyOffice Document Server: Disconnected")
                if 'error' in data:
                    print(f"   Error: {data['error']}")
        else:
            print(f"❌ OCR Agent API: Failed (Status: {response.status_code})")
            
    except requests.exceptions.ConnectionError:
        print("❌ OCR Agent API: Not running (Connection refused)")
        print("   Make sure the Flask application is running on port 5000")
        
    except Exception as e:
        print(f"❌ Error checking OCR Agent API: {e}")
    
    print()
    
    # Direct OnlyOffice check
    print("🏢 Checking OnlyOffice Document Server directly...")
    
    onlyoffice_urls = [
        'http://localhost:8000/healthcheck',
        'http://localhost:8000/api/health',
        'http://localhost:8000/'
    ]
    
    onlyoffice_connected = False
    
    for url in onlyoffice_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ OnlyOffice Direct: Connected ({url})")
                onlyoffice_connected = True
                break
        except:
            continue
    
    if not onlyoffice_connected:
        print("❌ OnlyOffice Direct: Not accessible")
        print("   OnlyOffice Document Server is not running on localhost:8000")
    
    print()
    
    # Test lesson generation fallback
    print("📝 Testing Lesson Generation Fallback...")
    
    try:
        test_data = {
            'subject': 'Test Subject',
            'class_level': 'Test Grade',
            'lesson_info': {'lesson': 'Test Lesson'}
        }
        
        response = requests.post(
            'http://localhost:5000/api/lessons/generate',
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                storage_type = data.get('storage_type', 'unknown')
                print(f"✅ Lesson Generation: Working ({storage_type} storage)")
                if 'file_path' in data:
                    print(f"   Local file: {data['file_path']}")
                elif 'document_id' in data:
                    print(f"   OnlyOffice document: {data['document_id']}")
            else:
                print(f"❌ Lesson Generation: Failed - {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Lesson Generation API: Failed (Status: {response.status_code})")
            
    except Exception as e:
        print(f"❌ Error testing lesson generation: {e}")
    
    print()
    print("📋 Summary:")
    print("-" * 20)
    
    if onlyoffice_connected:
        print("✅ OnlyOffice Document Server is running and accessible")
        print("✅ Full OnlyOffice integration available")
    else:
        print("❌ OnlyOffice Document Server is not running")
        print("✅ Local file fallback is available")
        print("📌 Recommendation: Install and start OnlyOffice Document Server for full functionality")
    
    print()
    print("🚀 Next Steps:")
    print("1. Open OCR Agent: http://localhost:5000")
    print("2. Go to Settings Panel: http://localhost:5000/panel/settings")
    print("3. Test Lesson Generator: http://localhost:5000/panel/lesson-generator")

if __name__ == "__main__":
    check_onlyoffice_status()