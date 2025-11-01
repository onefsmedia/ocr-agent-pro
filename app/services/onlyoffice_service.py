"""
OnlyOffice Service Integration for OCR Agent Pro
Handles both local file mode and Document Server integration
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from werkzeug.utils import secure_filename

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class OnlyOfficeService:
    """Service for handling OnlyOffice document editing integration"""
    
    def __init__(self):
        self.load_settings()
    
    def load_settings(self):
        """Load OnlyOffice settings from database or defaults"""
        try:
            from app.models import SystemSettings
            self.enabled = self.get_setting('onlyoffice_enabled', 'false') == 'true'
            self.mode = self.get_setting('onlyoffice_mode', 'local_files')
            self.server_url = self.get_setting('onlyoffice_server_url', 'http://localhost:8000')
            self.jwt_secret = self.get_setting('onlyoffice_jwt_secret', 'ocr-agent-secret-key-2025')
            self.jwt_header = self.get_setting('onlyoffice_jwt_header', 'Authorization')
            self.jwt_in_body = self.get_setting('onlyoffice_jwt_in_body', 'true') == 'true'
            
            self.storage_path = Path(self.get_setting('onlyoffice_storage_path', 'storage/documents'))
            self.temp_path = Path(self.get_setting('onlyoffice_temp_path', 'storage/temp'))
            self.callback_url = self.get_setting('onlyoffice_callback_url', 'http://localhost:5000/api/onlyoffice/callback')
            self.storage_url = self.get_setting('onlyoffice_storage_url', 'http://localhost:5000/storage')
            
            self.allowed_extensions = self.get_setting('onlyoffice_allowed_extensions', 'doc,docx,xls,xlsx,ppt,pptx,pdf,txt,rtf,odt,ods,odp').split(',')
            self.max_file_size = int(self.get_setting('onlyoffice_max_file_size', '52428800'))  # 50MB
            self.document_type = self.get_setting('onlyoffice_document_type', 'word')
            self.lang = self.get_setting('onlyoffice_lang', 'en')
        except ImportError:
            # Fallback if models are not available
            self.enabled = False
            self.mode = 'local_files'
            self.server_url = 'http://localhost:8000'
            self.jwt_secret = 'ocr-agent-secret-key-2025'
            self.jwt_header = 'Authorization'
            self.jwt_in_body = True
            
            self.storage_path = Path('storage/documents')
            self.temp_path = Path('storage/temp')
            self.callback_url = 'http://localhost:5000/api/onlyoffice/callback'
            self.storage_url = 'http://localhost:5000/storage'
            
            self.allowed_extensions = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'txt', 'rtf', 'odt', 'ods', 'odp']
            self.max_file_size = 52428800  # 50MB
            self.document_type = 'word'
            self.lang = 'en'
        
        # Ensure directories exist
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)
    
    def get_setting(self, key: str, default: str) -> str:
        """Get setting from database or return default"""
        try:
            from app.models import SystemSettings
            setting = SystemSettings.query.filter_by(key=key).first()
            return setting.value if setting else default
        except:
            return default
    
    def is_available(self) -> bool:
        """Check if OnlyOffice integration is available"""
        return self.enabled and (self.mode == 'local_files' or self.check_document_server())
    
    def check_document_server(self) -> bool:
        """Check if OnlyOffice Document Server is accessible"""
        if self.mode != 'document_server' or not REQUESTS_AVAILABLE:
            return False
        
        try:
            response = requests.get(f"{self.server_url}/healthcheck", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """Get supported document formats by category"""
        return {
            'word': ['doc', 'docx', 'odt', 'rtf', 'txt'],
            'cell': ['xls', 'xlsx', 'ods'],
            'slide': ['ppt', 'pptx', 'odp'],
            'pdf': ['pdf']
        }
    
    def get_document_type(self, filename: str) -> str:
        """Determine document type based on file extension"""
        ext = Path(filename).suffix.lower().lstrip('.')
        formats = self.get_supported_formats()
        
        for doc_type, extensions in formats.items():
            if ext in extensions:
                return doc_type
        
        return 'word'  # Default
    
    def can_edit_file(self, filename: str, file_size: int = 0) -> Tuple[bool, str]:
        """Check if file can be edited with OnlyOffice"""
        if not self.enabled:
            return False, "OnlyOffice integration is disabled"
        
        # Check file extension
        ext = Path(filename).suffix.lower().lstrip('.')
        if ext not in self.allowed_extensions:
            return False, f"File type '{ext}' is not supported"
        
        # Check file size
        if file_size > self.max_file_size:
            return False, f"File size exceeds maximum limit ({self.max_file_size / 1024 / 1024:.1f} MB)"
        
        # Check if Document Server is available (for server mode)
        if self.mode == 'document_server' and not self.check_document_server():
            return False, "OnlyOffice Document Server is not accessible"
        
        return True, "File can be edited"
    
    def prepare_document_for_editing(self, document_id: str, filename: str, file_content: bytes) -> Dict:
        """Prepare document for OnlyOffice editing"""
        try:
            # Secure filename
            safe_filename = secure_filename(filename)
            doc_type = self.get_document_type(safe_filename)
            
            # Create unique document key
            document_key = f"{document_id}_{safe_filename}"
            
            # Save file to storage
            file_path = self.storage_path / document_key
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Generate document URL
            document_url = f"{self.storage_url}/documents/{document_key}"
            
            if self.mode == 'local_files':
                return self._prepare_local_mode_config(document_key, safe_filename, doc_type, document_url)
            else:
                return self._prepare_server_mode_config(document_key, safe_filename, doc_type, document_url)
        
        except Exception as e:
            return {'error': f"Failed to prepare document: {str(e)}"}
    
    def _prepare_local_mode_config(self, document_key: str, filename: str, doc_type: str, document_url: str) -> Dict:
        """Prepare configuration for local file mode"""
        return {
            'success': True,
            'mode': 'local_files',
            'message': 'Document prepared for local editing',
            'config': {
                'document': {
                    'fileType': Path(filename).suffix.lower().lstrip('.'),
                    'key': document_key,
                    'title': filename,
                    'url': document_url,
                    'info': {
                        'owner': 'OCR Agent Pro',
                        'uploaded': True
                    }
                },
                'documentType': doc_type,
                'editorConfig': {
                    'mode': 'edit',
                    'lang': self.lang,
                    'callbackUrl': self.callback_url,
                    'user': {
                        'id': 'ocr-agent-user',
                        'name': 'OCR Agent User'
                    }
                },
                'width': '100%',
                'height': '600px'
            }
        }
    
    def _prepare_server_mode_config(self, document_key: str, filename: str, doc_type: str, document_url: str) -> Dict:
        """Prepare configuration for Document Server mode"""
        config = {
            'document': {
                'fileType': Path(filename).suffix.lower().lstrip('.'),
                'key': document_key,
                'title': filename,
                'url': document_url,
                'permissions': {
                    'comment': True,
                    'download': True,
                    'edit': True,
                    'fillForms': True,
                    'modifyFilter': True,
                    'modifyContentControl': True,
                    'review': True
                }
            },
            'documentType': doc_type,
            'editorConfig': {
                'mode': 'edit',
                'lang': self.lang,
                'callbackUrl': self.callback_url,
                'user': {
                    'id': 'ocr-agent-user',
                    'name': 'OCR Agent User'
                },
                'customization': {
                    'autosave': True,
                    'forcesave': False,
                    'compactToolbar': False
                }
            },
            'width': '100%',
            'height': '600px'
        }
        
        # Add JWT if enabled
        if self.jwt_secret:
            token = self._generate_jwt_token(config)
            config['token'] = token
        
        return {
            'success': True,
            'mode': 'document_server',
            'message': 'Document prepared for server editing',
            'config': config
        }
    
    def _generate_jwt_token(self, payload: Dict) -> str:
        """Generate JWT token for OnlyOffice authentication"""
        try:
            import jwt
            return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        except ImportError:
            # Fallback if PyJWT is not available
            import base64
            import json
            
            # Simple base64 encoding (not secure, but works for development)
            payload_str = json.dumps(payload, separators=(',', ':'))
            return base64.b64encode(payload_str.encode()).decode()
        except Exception as e:
            return ""
    
    def handle_callback(self, data: Dict) -> Dict:
        """Handle OnlyOffice Document Server callback"""
        try:
            status = data.get('status', 0)
            document_key = data.get('key', '')
            url = data.get('url', '')
            
            if status == 2:  # Document ready for saving
                return self._save_document_from_callback(document_key, url)
            elif status == 3:  # Document saving error
                return {'error': 'Document saving failed'}
            elif status == 4:  # Document closed with no changes
                return {'success': True, 'message': 'Document closed without changes'}
            
            return {'success': True, 'message': 'Callback processed'}
        
        except Exception as e:
            return {'error': f"Callback processing failed: {str(e)}"}
    
    def _save_document_from_callback(self, document_key: str, download_url: str) -> Dict:
        """Save document from OnlyOffice callback"""
        try:
            if not REQUESTS_AVAILABLE:
                return {'error': 'Requests library not available for document download'}
            
            # Download document from OnlyOffice
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            # Save to storage
            file_path = self.storage_path / document_key
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            return {
                'success': True,
                'message': 'Document saved successfully',
                'document_key': document_key,
                'file_path': str(file_path)
            }
        
        except Exception as e:
            return {'error': f"Failed to save document: {str(e)}"}
    
    def get_document_content(self, document_key: str) -> Optional[bytes]:
        """Get document content from storage"""
        try:
            file_path = self.storage_path / document_key
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    return f.read()
            return None
        except Exception:
            return None
    
    def delete_document(self, document_key: str) -> bool:
        """Delete document from storage"""
        try:
            file_path = self.storage_path / document_key
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def get_status(self) -> Dict:
        """Get OnlyOffice service status"""
        return {
            'enabled': self.enabled,
            'mode': self.mode,
            'server_available': self.check_document_server() if self.mode == 'document_server' else None,
            'storage_path': str(self.storage_path),
            'temp_path': str(self.temp_path),
            'supported_formats': self.get_supported_formats(),
            'max_file_size_mb': self.max_file_size / 1024 / 1024,
            'requests_available': REQUESTS_AVAILABLE,
            'message': self._get_status_message()
        }
    
    def _get_status_message(self) -> str:
        """Get human-readable status message"""
        if not self.enabled:
            return "OnlyOffice integration is disabled"
        
        if self.mode == 'local_files':
            return "Running in local file mode (basic functionality)"
        elif self.mode == 'document_server':
            if self.check_document_server():
                return "Document Server is accessible and ready"
            else:
                return "Document Server is not accessible"
        
        return "Unknown mode"

# Global service instance
onlyoffice_service = OnlyOfficeService()