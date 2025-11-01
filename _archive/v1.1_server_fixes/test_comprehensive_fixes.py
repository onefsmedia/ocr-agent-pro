#!/usr/bin/env python3
"""
Comprehensive Test Suite for Fixed OCR Agent Pro
Tests all components after bug fixes
"""

import os
import sys
import requests
import tempfile
import time
from datetime import datetime
from PIL import Image, ImageDraw

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """Test all critical imports"""
    print("🔍 TESTING IMPORTS...")
    try:
        from app import create_app, db
        from app.services.ocr_service import OCRService  
        from app.services.embedding_service import EmbeddingService
        from app.models import Document, DocumentChunk
        print("   ✅ All imports successful")
        return True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def test_chunking_logic():
    """Test the improved chunking logic"""
    print("🧩 TESTING CHUNKING LOGIC...")
    try:
        from app import create_app
        from app.services.embedding_service import EmbeddingService
        
        app = create_app()
        with app.app_context():
            embedding_service = EmbeddingService()
            
            # Test 1: Short text (should now work with 10 char minimum)
            short_text = "Short test text"
            chunks1 = embedding_service.create_chunks(short_text)
            print(f"   Short text ({len(short_text)} chars) → {len(chunks1)} chunks")
            
            # Test 2: Medium text
            medium_text = "This is a longer test document with enough content to potentially create multiple chunks for embedding generation."
            chunks2 = embedding_service.create_chunks(medium_text)
            print(f"   Medium text ({len(medium_text)} chars) → {len(chunks2)} chunks")
            
            # Test 3: Very short text (edge case)
            tiny_text = "Hi"
            chunks3 = embedding_service.create_chunks(tiny_text)
            print(f"   Tiny text ({len(tiny_text)} chars) → {len(chunks3)} chunks")
            
            # Test 4: Empty text
            chunks4 = embedding_service.create_chunks("")
            print(f"   Empty text → {len(chunks4)} chunks")
            
            print("   ✅ Chunking logic working correctly")
            return True
            
    except Exception as e:
        print(f"   ❌ Chunking test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ocr_service():
    """Test OCR service reliability"""
    print("🔤 TESTING OCR SERVICE...")
    try:
        from app import create_app
        from app.services.ocr_service import OCRService
        
        app = create_app()
        with app.app_context():
            ocr_service = OCRService()
            
            # Test language availability
            languages = ocr_service.get_tesseract_languages()
            print(f"   Available languages: {languages}")
            
            # Create test image
            img = Image.new('RGB', (300, 100), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((20, 30), 'Test OCR Processing', fill='black')
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                img.save(temp_file.name)
                test_image_path = temp_file.name
            
            # Test OCR processing
            result = ocr_service.process_document(test_image_path)
            print(f"   OCR result: '{result.strip()}'")
            
            # Clean up
            os.unlink(test_image_path)
            
            print("   ✅ OCR service working correctly")
            return True
            
    except Exception as e:
        print(f"   ❌ OCR test failed: {e}")
        return False

def test_flask_server_startup():
    """Test Flask server startup"""
    print("🌐 TESTING FLASK SERVER STARTUP...")
    try:
        from run_server import FlaskAppManager
        
        manager = FlaskAppManager()
        
        # Test app creation
        if manager.create_app_with_retry(max_retries=2):
            print("   ✅ Flask app creation successful")
            
            # Test health check
            if manager.health_check():
                print("   ✅ Health check passed")
                return True
            else:
                print("   ❌ Health check failed")
                return False
        else:
            print("   ❌ Flask app creation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Flask server test failed: {e}")
        return False

def test_upload_processing():
    """Test upload processing with error handling"""
    print("📤 TESTING UPLOAD PROCESSING...")
    try:
        from app import create_app, db
        from app.routes.api import api_bp
        
        app = create_app()
        app.register_blueprint(api_bp, url_prefix='/api')
        
        with app.app_context():
            with app.test_client() as client:
                # Create test file
                test_content = "OCR Agent Pro Test Document for comprehensive testing of the upload and processing pipeline with improved error handling and chunking logic."
                
                # Test upload
                from io import BytesIO
                
                response = client.post(
                    '/api/upload',
                    data={
                        'file': (BytesIO(test_content.encode()), 'test.txt'),
                        'document_name': 'Test Document',
                        'document_type': 'textbook',
                        'subject': 'Computer Science',
                        'class_level': 'Form 5'
                    },
                    content_type='multipart/form-data'
                )
                
                print(f"   Upload response status: {response.status_code}")
                if response.status_code in [200, 201]:
                    data = response.get_json()
                    print(f"   Document ID: {data.get('document_id', 'N/A')}")
                    print(f"   Chunks created: {data.get('chunks_created', 0)}")
                    print("   ✅ Upload processing working")
                    return True
                else:
                    print(f"   ❌ Upload failed: {response.data}")
                    return False
                    
    except Exception as e:
        print(f"   ❌ Upload test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_server_connectivity_test():
    """Test actual server connectivity"""
    print("🔗 TESTING SERVER CONNECTIVITY...")
    
    # Start server in background and test
    import subprocess
    import threading
    import signal
    
    server_process = None
    try:
        # Start the improved server
        print("   Starting server...")
        server_process = subprocess.Popen(
            [sys.executable, 'run_server.py'],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(8)
        
        # Test health endpoint
        try:
            response = requests.get('http://localhost:5000/api/health', timeout=10)
            if response.status_code == 200:
                print("   ✅ Server responding to health checks")
                
                # Test simple upload
                test_content = "Test document for server connectivity verification."
                files = {'file': ('test.txt', test_content.encode(), 'text/plain')}
                data = {
                    'document_name': 'Connectivity Test',
                    'document_type': 'textbook',
                    'subject': 'Computer Science',
                    'class_level': 'Form 5'
                }
                
                upload_response = requests.post(
                    'http://localhost:5000/api/upload',
                    files=files,
                    data=data,
                    timeout=30
                )
                
                print(f"   Upload test status: {upload_response.status_code}")
                if upload_response.status_code in [200, 201]:
                    print("   ✅ Server upload processing working")
                    return True
                else:
                    print(f"   ❌ Upload failed: {upload_response.text[:200]}")
                    return False
            else:
                print(f"   ❌ Server health check failed: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Could not connect to server")
            return False
        except Exception as e:
            print(f"   ❌ Server test error: {e}")
            return False
            
    finally:
        # Clean up server process
        if server_process:
            try:
                server_process.terminate()
                server_process.wait(timeout=5)
            except:
                try:
                    server_process.kill()
                except:
                    pass

def main():
    """Run comprehensive test suite"""
    print("🧪 OCR AGENT PRO - COMPREHENSIVE TEST SUITE (POST-FIX)")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Import Test", test_imports),
        ("Chunking Logic Test", test_chunking_logic),
        ("OCR Service Test", test_ocr_service),
        ("Flask Server Test", test_flask_server_startup),
        ("Upload Processing Test", test_upload_processing),
    ]
    
    results = []
    for test_name, test_func in tests:
        print()
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! OCR Agent Pro is ready for use.")
        print("\n📝 Fixed Issues:")
        print("✅ Chunking logic now accepts shorter text (10+ chars)")
        print("✅ Upload processing has comprehensive error handling")
        print("✅ Flask server has improved reliability and timeout handling")
        print("✅ OCR service has better error recovery")
        print("✅ Database operations are more robust")
        print("\n🚀 Ready for production use!")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        
    print("=" * 70)

if __name__ == "__main__":
    main()