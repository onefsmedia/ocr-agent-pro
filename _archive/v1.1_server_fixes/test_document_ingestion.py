#!/usr/bin/env python3
"""
Document Ingestion Test Suite
Tests the OCR Agent Pro system's ability to handle large documents
"""

import os
import sys
import requests
import time
from datetime import datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_current_config():
    """Test current Flask configuration limits"""
    print("🔍 CHECKING CURRENT CONFIGURATION")
    print("=" * 50)
    
    try:
        from app import create_app
        
        app = create_app()
        with app.app_context():
            max_size = app.config.get('MAX_CONTENT_LENGTH', 0)
            upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
            
            print(f"📁 Upload Folder: {upload_folder}")
            print(f"📏 Current Max File Size: {max_size / (1024*1024):.1f} MB")
            
            # Check if upload folder exists
            if os.path.exists(upload_folder):
                print(f"✅ Upload folder exists")
                
                # Check available disk space
                try:
                    import shutil
                    total, used, free = shutil.disk_usage(upload_folder)
                    free_gb = free / (1024**3)
                    print(f"💾 Available disk space: {free_gb:.1f} GB")
                    
                    if free_gb > 2:  # At least 2GB free for 500MB files
                        print("✅ Sufficient disk space for large files")
                    else:
                        print("⚠️ Limited disk space")
                        
                except Exception as e:
                    print(f"⚠️ Could not check disk space: {e}")
            else:
                print(f"❌ Upload folder does not exist")
                
            return max_size
            
    except Exception as e:
        print(f"❌ Configuration check failed: {e}")
        return 0

def test_flask_server_status():
    """Test if Flask server is running"""
    print("\n🌐 CHECKING FLASK SERVER STATUS")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Flask server is running")
            print(f"   Status: {data.get('status')}")
            print(f"   Database: {data.get('database')}")
            return True
        else:
            print(f"⚠️ Server responding with status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Flask server is not running")
        print("   Please start with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Server check failed: {e}")
        return False

def create_test_files():
    """Create test files of various sizes"""
    print("\n📝 CREATING TEST FILES")
    print("=" * 30)
    
    test_files = []
    
    # Small test file (1MB)
    try:
        small_file = "test_1mb.txt"
        with open(small_file, 'w') as f:
            # Write approximately 1MB of text
            content = "OCR Agent Pro Test Document\n" * 50000
            f.write(content)
        
        size_mb = os.path.getsize(small_file) / (1024*1024)
        print(f"✅ Created {small_file}: {size_mb:.1f} MB")
        test_files.append((small_file, size_mb))
        
    except Exception as e:
        print(f"❌ Failed to create small test file: {e}")
    
    # Medium test file (50MB)
    try:
        medium_file = "test_50mb.txt"
        with open(medium_file, 'w') as f:
            # Write approximately 50MB of text
            content = "OCR Agent Pro Large Document Test - " + "A" * 1000 + "\n"
            for i in range(50000):
                f.write(f"Line {i}: {content}")
        
        size_mb = os.path.getsize(medium_file) / (1024*1024)
        print(f"✅ Created {medium_file}: {size_mb:.1f} MB")
        test_files.append((medium_file, size_mb))
        
    except Exception as e:
        print(f"❌ Failed to create medium test file: {e}")
    
    return test_files

def test_upload_api(test_files, current_limit_mb):
    """Test upload API with different file sizes"""
    print("\n🚀 TESTING UPLOAD API")
    print("=" * 30)
    
    results = []
    
    for filename, size_mb in test_files:
        print(f"\nTesting {filename} ({size_mb:.1f} MB):")
        
        if size_mb > current_limit_mb:
            print(f"⚠️ File exceeds current limit ({current_limit_mb:.1f} MB)")
            print("   This test will likely fail with current configuration")
        
        try:
            # Prepare the upload
            with open(filename, 'rb') as f:
                files = {'file': (filename, f, 'text/plain')}
                data = {
                    'document_name': f'Test Document {filename}',
                    'document_type': 'textbook',
                    'subject': 'Computer Science',
                    'class_level': 'Form 5'
                }
                
                start_time = time.time()
                
                # Make the upload request with longer timeout
                response = requests.post(
                    'http://localhost:5000/api/upload',
                    files=files,
                    data=data,
                    timeout=300  # 5 minutes timeout for large files
                )
                
                end_time = time.time()
                upload_time = end_time - start_time
                
                if response.status_code == 201:
                    result_data = response.json()
                    print(f"✅ Upload successful!")
                    print(f"   Document ID: {result_data.get('document_id')}")
                    print(f"   Chunks created: {result_data.get('chunks_created')}")
                    print(f"   Upload time: {upload_time:.1f} seconds")
                    results.append((filename, size_mb, True, upload_time))
                else:
                    print(f"❌ Upload failed: HTTP {response.status_code}")
                    print(f"   Error: {response.text}")
                    results.append((filename, size_mb, False, upload_time))
                    
        except requests.exceptions.Timeout:
            print(f"⏱️ Upload timed out after 5 minutes")
            results.append((filename, size_mb, False, 300))
        except Exception as e:
            print(f"❌ Upload error: {e}")
            results.append((filename, size_mb, False, 0))
            
        # Clean up test file
        try:
            os.remove(filename)
        except:
            pass
    
    return results

def recommend_configuration():
    """Recommend configuration changes for 500MB support"""
    print("\n💡 RECOMMENDATIONS FOR 500MB DOCUMENT SUPPORT")
    print("=" * 55)
    
    print("📋 Required Configuration Changes:")
    print()
    print("1. Flask Configuration (config.py):")
    print("   MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB")
    print()
    print("2. Web Server Configuration:")
    print("   - Nginx: client_max_body_size 500M;")
    print("   - Apache: LimitRequestBody 524288000")
    print()
    print("3. System Requirements:")
    print("   - Available RAM: At least 2GB free")
    print("   - Disk Space: At least 2GB free")
    print("   - Processing time: 5-15 minutes per document")
    print()
    print("4. OCR Processing:")
    print("   - Large PDFs may need to be split into chunks")
    print("   - Consider background processing for files > 50MB")
    print("   - Monitor memory usage during OCR")
    print()
    print("5. Database Considerations:")
    print("   - Text fields can handle large content")
    print("   - Consider chunking strategy for embeddings")
    print("   - Monitor PostgreSQL memory usage")

def main():
    """Main testing function"""
    print("🧪 OCR AGENT PRO - DOCUMENT INGESTION TEST SUITE")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Check current configuration
    current_limit_mb = test_current_config() / (1024*1024)
    
    # Test 2: Check Flask server
    server_running = test_flask_server_status()
    
    if not server_running:
        print("\n❌ Cannot proceed with tests - Flask server not running")
        print("   Please start the server with: python app.py")
        return
    
    # Test 3: Create test files
    test_files = create_test_files()
    
    if not test_files:
        print("\n❌ No test files created - cannot test uploads")
        return
    
    # Test 4: Test uploads
    results = test_upload_api(test_files, current_limit_mb)
    
    # Test 5: Summary and recommendations
    print("\n📊 TEST RESULTS SUMMARY")
    print("=" * 30)
    
    for filename, size_mb, success, upload_time in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status} {filename}: {size_mb:.1f} MB in {upload_time:.1f}s")
    
    # Show recommendations
    recommend_configuration()
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS TO ENABLE 500MB SUPPORT:")
    print("1. Update configuration for larger files")
    print("2. Test with progressively larger files")
    print("3. Monitor system resources during processing")
    print("4. Consider implementing progress tracking")
    print("=" * 60)

if __name__ == "__main__":
    main()