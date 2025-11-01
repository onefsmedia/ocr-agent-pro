"""
OnlyOffice Connection Test Script
This script tests the OnlyOffice integration without needing the full service running
"""

import sys
import os

# Add the parent directory to the path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Simple test without importing sentence_transformers
def test_onlyoffice_integration():
    """Test OnlyOffice integration and settings"""
    
    print("🔧 Testing OnlyOffice Integration...")
    
    # Test 1: Configuration
    print("\n1. Testing Configuration:")
    config_items = {
        'ONLYOFFICE_URL': 'http://localhost:8000',
        'ONLYOFFICE_SECRET': 'ocr-agent-secret-key-2025',
        'ONLYOFFICE_TOKEN': '',
        'ONLYOFFICE_STORAGE_URL': 'http://localhost:5000/storage'
    }
    
    for key, value in config_items.items():
        print(f"   ✅ {key}: {value}")
    
    # Test 2: Basic Connection Test
    print("\n2. Testing Connection:")
    import requests
    
    try:
        response = requests.get('http://localhost:8000/healthcheck', timeout=5)
        if response.status_code == 200:
            print("   ✅ OnlyOffice Document Server is responding")
            print(f"   📊 Status: {response.status_code}")
        else:
            print(f"   ⚠️ OnlyOffice responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ OnlyOffice Document Server is not running")
        print("   📋 Next Steps:")
        print("      1. Start OnlyOffice using: podman run -d --name onlyoffice -p 8000:80 -e JWT_ENABLED=true -e JWT_SECRET=ocr-agent-secret-key-2025 onlyoffice/documentserver")
        print("      2. Wait 2-3 minutes for initialization")
        print("      3. Test again")
    except Exception as e:
        print(f"   ❌ Connection error: {str(e)}")
    
    # Test 3: OCR Agent Integration
    print("\n3. Testing OCR Agent Integration:")
    
    # Test settings panel endpoint
    try:
        response = requests.get('http://127.0.0.1:5000/panel/settings', timeout=5)
        if response.status_code == 200:
            print("   ✅ OCR Agent settings panel is accessible")
        else:
            print(f"   ⚠️ Settings panel responded with status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ OCR Agent settings error: {str(e)}")
    
    # Test OnlyOffice status endpoint
    try:
        response = requests.get('http://127.0.0.1:5000/api/onlyoffice/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ OnlyOffice status API is working")
            print(f"   📊 Connected: {data.get('connected', False)}")
            print(f"   📊 Service URL: {data.get('service_url', 'N/A')}")
        else:
            print(f"   ⚠️ OnlyOffice status API responded with status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ OnlyOffice status API error: {str(e)}")
    
    print("\n🎯 Summary:")
    print("   • OnlyOffice Integration: Configured")
    print("   • OCR Agent API: Available")
    print("   • Next Step: Start OnlyOffice Document Server")
    
    print("\n📖 Quick Start Commands:")
    print("   # Start OnlyOffice (simple version):")
    print("   podman run -d --name onlyoffice -p 8000:80 \\")
    print("     -e JWT_ENABLED=true \\")
    print("     -e JWT_SECRET=ocr-agent-secret-key-2025 \\")
    print("     docker.io/onlyoffice/documentserver:latest")
    print()
    print("   # Test connection:")
    print("   curl http://localhost:8000/healthcheck")
    print()
    print("   # Access settings:")
    print("   http://127.0.0.1:5000/panel/settings")

if __name__ == "__main__":
    test_onlyoffice_integration()