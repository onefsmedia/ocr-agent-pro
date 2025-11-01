#!/usr/bin/env python3
"""
Quick script to check document status in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import Document, db
from datetime import datetime

def check_documents():
    app = create_app()
    
    with app.app_context():
        # Get the most recent documents
        documents = Document.query.order_by(Document.created_at.desc()).limit(5).all()
        
        print("Recent Documents:")
        print("="*80)
        print(f"{'ID':<5} {'Filename':<30} {'Size (MB)':<12} {'Status':<15} {'Created At'}")
        print("-"*80)
        
        for doc in documents:
            size_mb = round(doc.file_size / (1024 * 1024), 1) if doc.file_size else 0
            created_at = doc.created_at.strftime("%Y-%m-%d %H:%M:%S") if doc.created_at else "Unknown"
            print(f"{str(doc.id)[:8]:<5} {doc.filename[:29]:<30} {size_mb:<12} {doc.processing_status or 'None':<15} {created_at}")
        
        # Find the Form 1 document specifically
        print("\nForm 1 Document Details:")
        print("="*50)
        form1_doc = Document.query.filter(Document.filename.like('%Form_1%')).order_by(Document.created_at.desc()).first()
        if form1_doc:
            print(f"ID: {form1_doc.id}")
            print(f"Filename: {form1_doc.filename}")
            print(f"Processing Status: {form1_doc.processing_status}")
            print(f"Extracted Text Length: {len(form1_doc.extracted_text) if form1_doc.extracted_text else 0} characters")
            print(f"Created At: {form1_doc.created_at}")
            
            # Check if there are document chunks
            from app.models import DocumentChunk
            chunks = DocumentChunk.query.filter_by(document_id=form1_doc.id).count()
            print(f"Number of chunks: {chunks}")
        else:
            print("No Form 1 document found")

if __name__ == "__main__":
    check_documents()