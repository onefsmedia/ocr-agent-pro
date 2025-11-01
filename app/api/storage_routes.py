"""
Simple OnlyOffice storage service for document management
"""

from flask import Blueprint, request, jsonify, send_file
import os
import json
import base64
from datetime import datetime

storage_bp = Blueprint('storage', __name__)

# Simple in-memory storage for demo purposes
# In production, this would be a proper database or file system
DOCUMENT_STORAGE = {}

@storage_bp.route('/storage/<doc_id>.docx', methods=['GET'])
def get_document(doc_id):
    """Retrieve a document for OnlyOffice"""
    try:
        if doc_id not in DOCUMENT_STORAGE:
            return jsonify({'error': 'Document not found'}), 404
        
        doc_data = DOCUMENT_STORAGE[doc_id]
        
        # For demo purposes, return a simple text response
        # In production, this would return the actual DOCX file
        return jsonify({
            'content': doc_data.get('content', ''),
            'title': doc_data.get('title', 'Untitled'),
            'last_modified': doc_data.get('last_modified', datetime.now().isoformat())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@storage_bp.route('/storage/<doc_id>', methods=['POST'])
def store_document(doc_id):
    """Store a document"""
    try:
        data = request.get_json()
        
        DOCUMENT_STORAGE[doc_id] = {
            'content': data.get('content', ''),
            'title': data.get('title', 'Untitled'),
            'last_modified': datetime.now().isoformat(),
            'created_at': DOCUMENT_STORAGE.get(doc_id, {}).get('created_at', datetime.now().isoformat())
        }
        
        return jsonify({
            'success': True,
            'document_id': doc_id,
            'message': 'Document stored successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@storage_bp.route('/storage/callback/<doc_id>', methods=['POST'])
def onlyoffice_callback(doc_id):
    """Handle OnlyOffice document save callbacks"""
    try:
        data = request.get_json()
        
        # OnlyOffice callback statuses:
        # 1 - document being edited
        # 2 - document ready for saving
        # 3 - document saving error
        # 6 - document being edited, force save
        # 7 - document force save error
        
        status = data.get('status', 0)
        
        if status == 2 or status == 6:  # Ready for saving or force save
            download_url = data.get('url')
            if download_url:
                # In a real implementation, you would download the document
                # from the URL and save it to your storage
                if doc_id in DOCUMENT_STORAGE:
                    DOCUMENT_STORAGE[doc_id]['last_modified'] = datetime.now().isoformat()
                
                return jsonify({'error': 0})  # Success
        
        return jsonify({'error': 0})  # Success for other statuses
        
    except Exception as e:
        print(f"OnlyOffice callback error: {e}")
        return jsonify({'error': 1}), 500  # Error

@storage_bp.route('/storage/list', methods=['GET'])
def list_documents():
    """List all stored documents"""
    try:
        documents = []
        for doc_id, doc_data in DOCUMENT_STORAGE.items():
            documents.append({
                'id': doc_id,
                'title': doc_data.get('title', 'Untitled'),
                'created_at': doc_data.get('created_at'),
                'last_modified': doc_data.get('last_modified'),
                'url': f"/storage/{doc_id}.docx"
            })
        
        return jsonify({
            'success': True,
            'documents': documents,
            'total': len(documents)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Helper function to create documents
def create_document_storage(doc_id, title, content):
    """Helper function to create a document in storage"""
    DOCUMENT_STORAGE[doc_id] = {
        'content': content,
        'title': title,
        'created_at': datetime.now().isoformat(),
        'last_modified': datetime.now().isoformat()
    }
    return True