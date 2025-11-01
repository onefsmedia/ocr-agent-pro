#!/usr/bin/env python3
"""
Comprehensive OnlyOffice port scanner and configuration
"""
import requests
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def scan_onlyoffice_ports():
    """Scan for OnlyOffice Document Server on various ports"""
    
    print("🔍 SCANNING FOR ONLYOFFICE DOCUMENT SERVER")
    print("=" * 50)
    
    # Common OnlyOffice ports and endpoints
    ports_to_test = [80, 8000, 8080, 8081, 8082, 8083, 9980, 443]
    endpoints_to_test = ['/', '/healthcheck', '/api/health', '/robots.txt', '/welcome']
    
    found_servers = []
    
    for port in ports_to_test:
        print(f"\n📡 Testing port {port}...")
        
        for endpoint in endpoints_to_test:
            urls = [f"http://localhost:{port}{endpoint}"]
            if port == 443:
                urls.append(f"https://localhost{endpoint}")
            
            for url in urls:
                try:
                    response = requests.get(url, timeout=3, verify=False)
                    content = response.text.lower()
                    
                    # Check for OnlyOffice indicators
                    onlyoffice_indicators = [
                        'onlyoffice', 'document server', 'documentserver', 
                        'converter', 'docservice', 'spellchecker'
                    ]
                    
                    is_onlyoffice = any(indicator in content for indicator in onlyoffice_indicators)
                    
                    if response.status_code == 200 and is_onlyoffice:
                        found_servers.append({
                            'url': url,
                            'status': response.status_code,
                            'type': 'OnlyOffice Document Server'
                        })
                        print(f"   ✅ {url} - OnlyOffice Document Server detected!")
                    elif response.status_code == 200:
                        print(f"   ℹ️  {url} - Server responding (not OnlyOffice)")
                    elif response.status_code in [401, 403]:
                        print(f"   🔒 {url} - Server responding (authentication required)")
                    
                except requests.exceptions.ConnectionError:
                    continue
                except requests.exceptions.Timeout:
                    continue
                except Exception as e:
                    continue
    
    print(f"\n📊 SCAN RESULTS:")
    print("=" * 30)
    
    if found_servers:
        print(f"✅ Found {len(found_servers)} OnlyOffice server(s):")
        for server in found_servers:
            print(f"   🌐 {server['url']} ({server['type']})")
        
        # Configure OCR Agent with the first found server
        best_server = found_servers[0]['url'].rstrip('/')
        configure_ocr_agent(best_server)
        return True
    else:
        print("❌ No OnlyOffice Document Server found")
        print("\n💡 Troubleshooting steps:")
        print("1. Restart OnlyOffice services as Administrator")
        print("2. Check Windows Firewall settings")
        print("3. Look for OnlyOffice logs in:")
        print("   C:\\Program Files\\ONLYOFFICE\\DocumentServer\\logs\\")
        return False

def configure_ocr_agent(server_url):
    """Configure OCR Agent with the detected OnlyOffice server"""
    
    try:
        from app import create_app, db
        from app.models import SystemSettings
        
        app = create_app()
        
        with app.app_context():
            print(f"\n🔧 Configuring OCR Agent with: {server_url}")
            
            settings = {
                'onlyoffice_server_url': server_url,
                'onlyoffice_enabled': 'true',
                'onlyoffice_mode': 'document_server'
            }
            
            for key, value in settings.items():
                setting = SystemSettings.query.filter_by(key=key).first()
                if setting:
                    setting.value = value
                else:
                    new_setting = SystemSettings(
                        key=key,
                        value=value,
                        setting_type='string',
                        description=f'OnlyOffice: {key}'
                    )
                    db.session.add(new_setting)
            
            db.session.commit()
            print("✅ OCR Agent configured successfully!")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")

if __name__ == "__main__":
    scan_onlyoffice_ports()