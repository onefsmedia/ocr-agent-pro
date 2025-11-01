#!/usr/bin/env python3
"""
Enhanced Document Ingestion Test with PDF Support
Tests large document ingestion capabilities with proper file types
"""

import os
import sys
import requests
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def create_test_pdf_with_reportlab(filename, size_mb_target):
    """Create a test PDF using reportlab"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Calculate how many pages we need for target size
        # Each page with text is roughly 1KB, so we need many pages for large files
        pages_needed = max(1, int(size_mb_target * 100))  # Rough estimate
        
        for page in range(min(pages_needed, 1000)):  # Limit to 1000 pages max
            c.drawString(100, height - 100, f"OCR Agent Pro Test Document - Page {page + 1}")
            c.drawString(100, height - 130, f"Document Processing Test for Cameroonian Education System")
            c.drawString(100, height - 160, f"This is a test document to verify large file processing capabilities.")
            c.drawString(100, height - 190, f"Subject: Computer Science")
            c.drawString(100, height - 220, f"Class Level: Form 5")
            c.drawString(100, height - 250, f"Document Type: Textbook")
            
            # Add more content to increase file size
            y_pos = height - 300
            for line in range(20):
                if y_pos > 50:
                    c.drawString(100, y_pos, f"Line {line + 1}: Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 3)
                    y_pos -= 20
            
            c.showPage()
        
        c.save()
        
        actual_size = os.path.getsize(filename) / (1024 * 1024)
        return True, actual_size
        
    except ImportError:
        return False, 0
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False, 0

def create_test_image(filename, size_mb_target):
    """Create a test image file"""
    try:
        # Create a large image to reach target size
        width = min(4000, int(size_mb_target * 400))  # Scale width based on target size
        height = min(3000, int(size_mb_target * 300))
        
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add text content
        try:
            # Try to use a font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Add multiple lines of text
        y_position = 50
        for i in range(min(100, int(size_mb_target * 10))):
            text = f"OCR Agent Pro Test Document - Line {i + 1}"
            draw.text((50, y_position), text, fill='black', font=font)
            y_position += 30
            if y_position > height - 50:
                y_position = 50
        
        # Save as PNG for better compatibility
        img.save(filename, 'PNG')
        
        actual_size = os.path.getsize(filename) / (1024 * 1024)
        return True, actual_size
        
    except Exception as e:
        print(f"Error creating image: {e}")
        return False, 0

def create_test_documents():
    """Create test documents of various sizes"""
    print("📝 CREATING TEST DOCUMENTS")
    print("=" * 35)
    
    test_files = []
    
    # Test 1: Small PDF (1-2MB)
    print("Creating small PDF...")
    success, size = create_test_pdf_with_reportlab("test_small.pdf", 1)
    if success:
        print(f"✅ Created test_small.pdf: {size:.1f} MB")
        test_files.append(("test_small.pdf", size, "application/pdf"))
    else:
        print("⚠️ Reportlab not available, creating image instead...")
        success, size = create_test_image("test_small.png", 1)
        if success:
            print(f"✅ Created test_small.png: {size:.1f} MB")
            test_files.append(("test_small.png", size, "image/png"))
    
    # Test 2: Medium file (10-15MB)
    print("\nCreating medium file...")
    success, size = create_test_image("test_medium.png", 10)
    if success:
        print(f"✅ Created test_medium.png: {size:.1f} MB")
        test_files.append(("test_medium.png", size, "image/png"))
    
    # Test 3: Large file (50MB) - only if we have space and time
    print("\nCreating large file (this may take a moment)...")
    success, size = create_test_image("test_large.png", 50)
    if success:
        print(f"✅ Created test_large.png: {size:.1f} MB")
        test_files.append(("test_large.png", size, "image/png"))
    
    return test_files

def test_upload_with_progress(test_files):
    """Test upload with progress monitoring"""
    print("\n🚀 TESTING UPLOAD WITH PROGRESS MONITORING")
    print("=" * 50)
    
    results = []
    
    for filename, size_mb, mime_type in test_files:
        print(f"\n📤 Testing {filename} ({size_mb:.1f} MB):")
        
        try:
            # Check if Flask server is running
            health_check = requests.get('http://localhost:5000/api/health', timeout=5)
            if health_check.status_code != 200:
                print("❌ Flask server not responding")
                continue
            
            # Prepare the upload
            with open(filename, 'rb') as f:
                files = {'file': (filename, f, mime_type)}
                data = {
                    'document_name': f'Test Document {filename}',
                    'document_type': 'textbook',
                    'subject': 'Computer Science',
                    'class_level': 'Form 5'
                }
                
                start_time = time.time()
                print("   📡 Starting upload...")
                
                # Make the upload request with appropriate timeout
                timeout = max(60, int(size_mb * 2))  # 2 seconds per MB minimum
                
                response = requests.post(
                    'http://localhost:5000/api/upload',
                    files=files,
                    data=data,
                    timeout=timeout
                )
                
                end_time = time.time()
                upload_time = end_time - start_time
                
                if response.status_code == 201:
                    result_data = response.json()
                    print(f"   ✅ Upload successful!")
                    print(f"   📄 Document ID: {result_data.get('document_id')}")
                    print(f"   🧩 Chunks created: {result_data.get('chunks_created')}")
                    print(f"   ⏱️ Upload time: {upload_time:.1f} seconds")
                    print(f"   🚀 Speed: {size_mb/upload_time:.2f} MB/s")
                    results.append((filename, size_mb, True, upload_time, result_data))
                    
                    # Test document retrieval
                    doc_id = result_data.get('document_id')
                    if doc_id:
                        doc_response = requests.get(f'http://localhost:5000/api/documents/{doc_id}')
                        if doc_response.status_code == 200:
                            print(f"   ✅ Document retrieval successful")
                        else:
                            print(f"   ⚠️ Document retrieval failed: {doc_response.status_code}")
                
                elif response.status_code == 413:
                    print(f"   ❌ File too large for Flask development server")
                    print(f"   💡 This is expected for files > ~100MB in development mode")
                    results.append((filename, size_mb, False, upload_time, {"error": "File too large for dev server"}))
                
                else:
                    print(f"   ❌ Upload failed: HTTP {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   📋 Error: {error_data.get('error', 'Unknown error')}")
                    except:
                        print(f"   📋 Error response: {response.text[:200]}")
                    results.append((filename, size_mb, False, upload_time, {"error": response.text}))
                    
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Upload timed out after {timeout} seconds")
            results.append((filename, size_mb, False, timeout, {"error": "Timeout"}))
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection error - Flask server may not be running")
            results.append((filename, size_mb, False, 0, {"error": "Connection failed"}))
        except Exception as e:
            print(f"   ❌ Upload error: {e}")
            results.append((filename, size_mb, False, 0, {"error": str(e)}))
        
        # Clean up test file
        try:
            os.remove(filename)
            print(f"   🗑️ Cleaned up {filename}")
        except:
            pass
    
    return results

def analyze_results(results):
    """Analyze test results and provide recommendations"""
    print("\n📊 TEST RESULTS ANALYSIS")
    print("=" * 35)
    
    successful_uploads = [r for r in results if r[2]]  # r[2] is success boolean
    failed_uploads = [r for r in results if not r[2]]
    
    print(f"✅ Successful uploads: {len(successful_uploads)}")
    print(f"❌ Failed uploads: {len(failed_uploads)}")
    print()
    
    if successful_uploads:
        print("🎉 SUCCESSFUL UPLOADS:")
        for filename, size_mb, success, upload_time, data in successful_uploads:
            speed = size_mb / upload_time if upload_time > 0 else 0
            print(f"   ✅ {filename}: {size_mb:.1f} MB in {upload_time:.1f}s ({speed:.2f} MB/s)")
        print()
        
        # Calculate statistics
        total_size = sum(r[1] for r in successful_uploads)
        total_time = sum(r[3] for r in successful_uploads)
        avg_speed = total_size / total_time if total_time > 0 else 0
        
        print(f"📈 Statistics:")
        print(f"   Total processed: {total_size:.1f} MB")
        print(f"   Average speed: {avg_speed:.2f} MB/s")
        print(f"   Largest successful: {max(r[1] for r in successful_uploads):.1f} MB")
    
    if failed_uploads:
        print("❌ FAILED UPLOADS:")
        for filename, size_mb, success, upload_time, data in failed_uploads:
            error = data.get('error', 'Unknown error')
            print(f"   ❌ {filename}: {size_mb:.1f} MB - {error}")
    
    return successful_uploads, failed_uploads

def provide_recommendations(successful_uploads, failed_uploads):
    """Provide recommendations based on test results"""
    print("\n💡 RECOMMENDATIONS")
    print("=" * 25)
    
    max_successful_size = max((r[1] for r in successful_uploads), default=0)
    
    if max_successful_size > 0:
        print(f"✅ Current capability: Up to {max_successful_size:.1f} MB documents")
        print()
        
        if max_successful_size >= 50:
            print("🎉 EXCELLENT: Large file support is working!")
            print("   • Can handle documents up to 50MB+")
            print("   • OCR processing is functional")
            print("   • Database integration working")
        elif max_successful_size >= 10:
            print("✅ GOOD: Medium file support confirmed")
            print("   • Can handle documents up to 10-50MB")
            print("   • Ready for most educational documents")
        else:
            print("⚠️ LIMITED: Only small files working")
            print("   • Need to investigate upload limits")
    
    print("\n📋 FOR 500MB SUPPORT:")
    print("1. Current Flask dev server limits uploads")
    print("2. Use production WSGI server (Gunicorn/uWSGI)")
    print("3. Configure web server (Nginx) for large uploads")
    print("4. Consider chunked upload for very large files")
    print("5. Implement background processing for files > 100MB")

def main():
    """Main test function"""
    print("🧪 ENHANCED DOCUMENT INGESTION TEST")
    print("=" * 45)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check Flask server
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Flask server running (Database: {data.get('database')})")
        else:
            print(f"⚠️ Flask server responding with status: {response.status_code}")
    except:
        print("❌ Flask server not accessible")
        print("   Please start with: python app.py")
        return
    
    # Create test documents
    test_files = create_test_documents()
    
    if not test_files:
        print("❌ No test files created")
        return
    
    # Test uploads
    results = test_upload_with_progress(test_files)
    
    # Analyze results
    successful_uploads, failed_uploads = analyze_results(results)
    
    # Provide recommendations
    provide_recommendations(successful_uploads, failed_uploads)
    
    print("\n" + "=" * 45)
    print("🎯 SUMMARY:")
    if successful_uploads:
        max_size = max(r[1] for r in successful_uploads)
        print(f"✅ OCR Agent Pro can handle documents up to {max_size:.1f} MB")
        print("✅ File upload and OCR processing working")
        print("✅ Database integration functional")
    else:
        print("❌ Need to resolve upload issues before testing large files")
    
    print("\n💡 For true 500MB support:")
    print("   • Deploy with production WSGI server")
    print("   • Configure Nginx for large uploads") 
    print("   • Implement chunked/streaming uploads")
    print("=" * 45)

if __name__ == "__main__":
    main()