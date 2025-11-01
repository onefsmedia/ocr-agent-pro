#!/usr/bin/env python3
"""
Test OnlyOffice Document Server connectivity and integration
"""

import requests
import json
from datetime import datetime

def test_onlyoffice_connectivity():
    """Test OnlyOffice Document Server endpoints"""
    print("🧪 TESTING ONLYOFFICE DOCUMENT SERVER CONNECTIVITY")
    print("=" * 55)
    
    base_url = "http://localhost:8096"
    
    # Test endpoints to check
    endpoints = [
        ("/", "Main page"),
        ("/welcome", "Welcome page"),
        ("/healthcheck", "Health check"),
        ("/coauthoring/CommandService.ashx", "Command service API")
    ]
    
    results = []
    
    for endpoint, description in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            print(f"Testing {description}: {url}")
            response = requests.get(url, timeout=10)
            status = "✅ SUCCESS" if response.status_code == 200 else f"⚠️ Status {response.status_code}"
            print(f"  {status}")
            results.append((endpoint, response.status_code, "OK"))
            
            # Show response content for API endpoints
            if endpoint == "/healthcheck":
                try:
                    content = response.text[:200]
                    print(f"  Response: {content}")
                except:
                    pass
                    
        except requests.exceptions.ConnectionError:
            print(f"  ❌ CONNECTION FAILED - Service not accessible")
            results.append((endpoint, None, "Connection Failed"))
        except requests.exceptions.Timeout:
            print(f"  ⏱️ TIMEOUT - Service may be starting")
            results.append((endpoint, None, "Timeout"))
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            results.append((endpoint, None, f"Error: {str(e)}"))
        
        print()
    
    # Summary
    print("📊 CONNECTIVITY TEST SUMMARY")
    print("-" * 30)
    
    success_count = sum(1 for _, status, _ in results if status == 200)
    total_count = len(results)
    
    for endpoint, status, note in results:
        status_icon = "✅" if status == 200 else "❌" 
        print(f"{status_icon} {endpoint}: {status or note}")
    
    print(f"\n🎯 Success Rate: {success_count}/{total_count}")
    
    if success_count >= 2:
        print("🎉 OnlyOffice Document Server appears to be working!")
        print("Ready for OCR Agent Pro integration!")
        return True
    else:
        print("⚠️ OnlyOffice Document Server may need more configuration")
        print("Please ensure the admin script was run successfully")
        return False

def test_ocr_agent_integration():
    """Test OCR Agent Pro OnlyOffice integration"""
    print("\n🔗 TESTING OCR AGENT PRO INTEGRATION")
    print("=" * 40)
    
    try:
        import os
        import sys
        
        # Add the project root to Python path
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        
        from app import create_app
        from app.models import SystemSettings
        from app.services.onlyoffice_service import OnlyOfficeService
        
        app = create_app()
        with app.app_context():
            # Check database settings
            settings = SystemSettings.query.filter(
                SystemSettings.key.like('onlyoffice_%')
            ).all()
            
            print("📋 OnlyOffice Settings in Database:")
            for setting in settings:
                print(f"  {setting.key}: {setting.value}")
            
            # Test OnlyOffice service
            print("\n🔧 Testing OnlyOffice Service:")
            service = OnlyOfficeService()
            service.load_settings()
            
            print(f"  Mode: {service.mode}")
            print(f"  Server URL: {service.server_url}")
            print(f"  API Endpoint: {service.api_endpoint}")
            
            # Test service status
            status = service.get_status()
            print(f"  Service Status: {status}")
            
            print("\n✅ OCR Agent Pro integration appears configured correctly!")
            return True
            
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test OnlyOffice connectivity
    connectivity_ok = test_onlyoffice_connectivity()
    
    # Test integration
    integration_ok = test_ocr_agent_integration()
    
    print("\n" + "=" * 60)
    if connectivity_ok and integration_ok:
        print("🎉 ALL TESTS PASSED! OnlyOffice integration is ready!")
        print("\nTo start using the system:")
        print("1. Run: python app.py")
        print("2. Access: http://localhost:5001")
        print("3. Upload documents and test OnlyOffice editing")
    else:
        print("⚠️ Some tests failed. Please check the configuration.")
        if not connectivity_ok:
            print("   - Run configure_onlyoffice_port_admin.ps1 as Administrator")
        if not integration_ok:
            print("   - Check database connection and models")
    
    print("\n" + "=" * 60)