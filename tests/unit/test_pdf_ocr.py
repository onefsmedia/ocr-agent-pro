#!/usr/bin/env python3
"""
Test script to verify Poppler integration with PDF OCR
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.ocr_service import OCRService

def test_pdf_ocr():
    app = create_app()
    
    with app.app_context():
        # Test with the Form 1 PDF document
        pdf_path = "c:\\OCR Agent\\uploads\\documents\\Form_1_-_English-T.pdf"
        
        if not os.path.exists(pdf_path):
            print(f"❌ PDF file not found at: {pdf_path}")
            return
        
        print(f"✅ Found PDF file: {pdf_path}")
        print(f"📁 File size: {os.path.getsize(pdf_path) / (1024*1024):.1f} MB")
        
        # Initialize OCR service
        ocr_service = OCRService()
        
        print("\n🔍 Testing PDF OCR with Poppler...")
        try:
            # Process the PDF document
            extracted_text = ocr_service.process_document(pdf_path)
            
            print(f"✅ OCR processing completed!")
            print(f"📝 Extracted text length: {len(extracted_text)} characters")
            
            if len(extracted_text) > 1000:
                print(f"📄 First 500 characters:")
                print("-" * 50)
                print(extracted_text[:500])
                print("-" * 50)
                print(f"... and {len(extracted_text) - 500} more characters")
            else:
                print(f"📄 Full extracted text:")
                print("-" * 50)
                print(extracted_text)
                print("-" * 50)
                
        except Exception as e:
            print(f"❌ OCR processing failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_pdf_ocr()