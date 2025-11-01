"""
OnlyOffice API routes for OCR Agent Pro
Handles document editing, callbacks, and file management
"""

from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import os
import tempfile
from pathlib import Path
from app.services.onlyoffice_service import onlyoffice_service
from app.models import Document, db
import uuid

onlyoffice_bp = Blueprint('onlyoffice', __name__, url_prefix='/api/onlyoffice')

@onlyoffice_bp.route('/status', methods=['GET'])
def get_status():
    """Get OnlyOffice service status"""
    try:
        status = onlyoffice_service.get_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@onlyoffice_bp.route('/supported-formats', methods=['GET'])
def get_supported_formats():
    """Get supported document formats"""
    try:
        formats = onlyoffice_service.get_supported_formats()
        return jsonify({
            'success': True,
            'formats': formats,
            'all_extensions': onlyoffice_service.allowed_extensions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@onlyoffice_bp.route('/edit/<int:document_id>', methods=['POST'])
def prepare_edit_document(document_id):
    """Prepare document for OnlyOffice editing"""
    try:
        # Get document from database
        document = Document.query.get_or_404(document_id)
        
        if not document.file_path or not os.path.exists(document.file_path):
            return jsonify({
                'success': False,
                'error': 'Document file not found'
            }), 404
        
        # Check if file can be edited
        file_size = os.path.getsize(document.file_path)
        can_edit, message = onlyoffice_service.can_edit_file(document.filename, file_size)
        
        if not can_edit:
            return jsonify({
                'success': False,
                'error': message
            }), 400
        
        # Read file content
        with open(document.file_path, 'rb') as f:
            file_content = f.read()
        
        # Prepare document for editing
        config = onlyoffice_service.prepare_document_for_editing(
            str(document_id),
            document.filename,
            file_content
        )
        
        if 'error' in config:
            return jsonify({
                'success': False,
                'error': config['error']
            }), 500
        
        return jsonify(config)
        
    except Exception as e:
        current_app.logger.error(f"Error preparing document for editing: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to prepare document for editing'
        }), 500

@onlyoffice_bp.route('/callback', methods=['POST'])
def document_callback():
    """Handle OnlyOffice Document Server callback"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No callback data received'}), 400
        
        # Process callback
        result = onlyoffice_service.handle_callback(data)
        
        if 'error' in result:
            current_app.logger.error(f"OnlyOffice callback error: {result['error']}")
            return jsonify(result), 400
        
        # If document was saved, update database
        if 'document_key' in result:
            # Extract document ID from key
            try:
                document_id = result['document_key'].split('_')[0]
                document = Document.query.get(int(document_id))
                
                if document:
                    # Update document metadata
                    document.modified_date = db.func.now()
                    db.session.commit()
                    
                    current_app.logger.info(f"Document {document_id} updated successfully")
            except (ValueError, IndexError):
                current_app.logger.warning(f"Could not extract document ID from key: {result['document_key']}")
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"OnlyOffice callback error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Callback processing failed'
        }), 500

@onlyoffice_bp.route('/storage/documents/<document_key>', methods=['GET'])
def serve_document(document_key):
    """Serve document file for OnlyOffice editor"""
    try:
        # Get document content from storage
        content = onlyoffice_service.get_document_content(document_key)
        
        if content is None:
            return jsonify({
                'success': False,
                'error': 'Document not found'
            }), 404
        
        # Extract filename from document key
        filename = '_'.join(document_key.split('_')[1:])
        
        # Create temporary file to serve
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            return send_file(
                temp_file_path,
                as_attachment=False,
                download_name=filename,
                mimetype='application/octet-stream'
            )
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
    except Exception as e:
        current_app.logger.error(f"Error serving document: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to serve document'
        }), 500

@onlyoffice_bp.route('/upload', methods=['POST'])
def upload_document():
    """Upload new document for OnlyOffice editing"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Secure filename
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({
                'success': False,
                'error': 'Invalid filename'
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        can_edit, message = onlyoffice_service.can_edit_file(filename, file_size)
        if not can_edit:
            return jsonify({
                'success': False,
                'error': message
            }), 400
        
        # Save file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Create document record
            document = Document(
                filename=filename,
                file_path=temp_file_path,
                file_size=file_size,
                document_type='office',
                upload_date=db.func.now()
            )
            
            db.session.add(document)
            db.session.commit()
            
            # Prepare for editing
            file_content = file.read()
            config = onlyoffice_service.prepare_document_for_editing(
                str(document.id),
                filename,
                file_content
            )
            
            if 'error' in config:
                # Clean up if preparation failed
                db.session.delete(document)
                db.session.commit()
                return jsonify({
                    'success': False,
                    'error': config['error']
                }), 500
            
            return jsonify({
                'success': True,
                'message': 'Document uploaded and ready for editing',
                'document_id': document.id,
                'config': config
            })
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
    except Exception as e:
        current_app.logger.error(f"Error uploading document: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to upload document'
        }), 500

@onlyoffice_bp.route('/download/<int:document_id>', methods=['GET'])
def download_document(document_id):
    """Download edited document"""
    try:
        # Get document from database
        document = Document.query.get_or_404(document_id)
        
        # Get document key
        document_key = f"{document_id}_{secure_filename(document.filename)}"
        
        # Get document content from OnlyOffice storage
        content = onlyoffice_service.get_document_content(document_key)
        
        if content is None:
            # Fallback to original file
            if document.file_path and os.path.exists(document.file_path):
                return send_file(
                    document.file_path,
                    as_attachment=True,
                    download_name=document.filename
                )
            else:
                return jsonify({
                    'success': False,
                    'error': 'Document not found'
                }), 404
        
        # Create temporary file for download
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(document.filename).suffix) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            return send_file(
                temp_file_path,
                as_attachment=True,
                download_name=document.filename
            )
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
    except Exception as e:
        current_app.logger.error(f"Error downloading document: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to download document'
        }), 500

@onlyoffice_bp.route('/delete/<document_key>', methods=['DELETE'])
def delete_document_storage(document_key):
    """Delete document from OnlyOffice storage"""
    try:
        success = onlyoffice_service.delete_document(document_key)
        
        return jsonify({
            'success': success,
            'message': 'Document deleted successfully' if success else 'Document not found'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error deleting document: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete document'
        }), 500

@onlyoffice_bp.route('/config', methods=['GET'])
def get_onlyoffice_config():
    """Get OnlyOffice editor configuration"""
    try:
        # Load current settings
        onlyoffice_service.load_settings()
        
        config = {
            'enabled': onlyoffice_service.enabled,
            'mode': onlyoffice_service.mode,
            'server_url': onlyoffice_service.server_url,
            'callback_url': onlyoffice_service.callback_url,
            'storage_url': onlyoffice_service.storage_url,
            'lang': onlyoffice_service.lang,
            'max_file_size_mb': onlyoffice_service.max_file_size / 1024 / 1024,
            'supported_formats': onlyoffice_service.get_supported_formats()
        }
        
        return jsonify({
            'success': True,
            'config': config
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting OnlyOffice config: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get configuration'
        }), 500

@onlyoffice_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@onlyoffice_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500