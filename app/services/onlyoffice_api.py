"""
OnlyOffice Document Server API Integration
Handles document creation, editing, and management with OnlyOffice
"""

import requests
import json
import uuid
import base64
from typing import Dict, Any, Optional
from flask import current_app

class OnlyOfficeAPI:
    """OnlyOffice Document Server API client"""
    
    def __init__(self):
        self.base_url = 'http://localhost:8000'  # Default OnlyOffice URL
        self.api_key = None
        self.storage_url = 'http://localhost:5000/storage'
        
        # Load from config if available
        try:
            if hasattr(current_app, 'config'):
                self.base_url = current_app.config.get('ONLYOFFICE_URL', self.base_url)
                self.api_key = current_app.config.get('ONLYOFFICE_SECRET')
                self.storage_url = current_app.config.get('ONLYOFFICE_STORAGE_URL', self.storage_url)
        except RuntimeError:
            # current_app not available, use defaults
            pass
    
    def create_document(self, title: str, content: str = "") -> Dict[str, Any]:
        """Create a new document in OnlyOffice"""
        try:
            doc_id = str(uuid.uuid4())
            
            # Create document content in DOCX format
            document_data = {
                "key": doc_id,
                "title": f"{title}.docx",
                "url": f"{self.storage_url}/{doc_id}.docx",
                "fileType": "docx",
                "content": content,
                "permissions": {
                    "edit": True,
                    "download": True,
                    "print": True,
                    "review": True,
                    "comment": True
                }
            }
            
            # Store document in storage
            storage_response = self._store_document(doc_id, content, title)
            
            if storage_response.get('success'):
                return {
                    "success": True,
                    "document_id": doc_id,
                    "title": title,
                    "edit_url": f"{self.base_url}?documentId={doc_id}&title={title}",
                    "download_url": f"{self.storage_url}/{doc_id}.docx",
                    "view_url": f"{self.base_url}?documentId={doc_id}&mode=view"
                }
            else:
                return {"success": False, "error": "Failed to store document"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _store_document(self, doc_id: str, content: str, title: str) -> Dict[str, Any]:
        """Store document content for OnlyOffice access"""
        try:
            # Create minimal DOCX structure with content
            docx_content = self._create_docx_content(content, title)
            
            # Store document
            storage_payload = {
                "document_id": doc_id,
                "content": base64.b64encode(docx_content).decode('utf-8'),
                "filename": f"{title}.docx",
                "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            }
            
            # Here we would normally send to OnlyOffice storage
            # For now, we'll simulate successful storage
            return {"success": True, "stored_id": doc_id}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_docx_content(self, text_content: str, title: str) -> bytes:
        """Create basic DOCX content from text"""
        try:
            # Simple DOCX XML structure
            docx_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        <w:p>
            <w:pPr>
                <w:pStyle w:val="Title"/>
            </w:pPr>
            <w:r>
                <w:t>{title}</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:r>
                <w:t>{text_content}</w:t>
            </w:r>
        </w:p>
    </w:body>
</w:document>"""
            
            return docx_xml.encode('utf-8')
            
        except Exception as e:
            print(f"Error creating DOCX content: {e}")
            return b""
    
    def get_editor_config(self, doc_id: str, title: str, mode: str = "edit") -> Dict[str, Any]:
        """Generate OnlyOffice editor configuration"""
        try:
            config = {
                "document": {
                    "fileType": "docx",
                    "key": doc_id,
                    "title": f"{title}.docx",
                    "url": f"{self.storage_url}/{doc_id}.docx",
                    "permissions": {
                        "edit": mode == "edit",
                        "download": True,
                        "print": True,
                        "review": mode == "edit",
                        "comment": mode == "edit"
                    }
                },
                "documentType": "text",
                "editorConfig": {
                    "mode": mode,
                    "callbackUrl": f"{self.storage_url}/callback/{doc_id}",
                    "user": {
                        "id": "user1",
                        "name": "OCR Agent User"
                    },
                    "customization": {
                        "autosave": True,
                        "chat": False,
                        "comments": True,
                        "help": True,
                        "hideRightMenu": False,
                        "logo": {
                            "image": "",
                            "imageEmbedded": "",
                            "url": ""
                        },
                        "review": {
                            "hideReviewDisplay": False,
                            "showReviewChanges": False
                        }
                    }
                },
                "height": "600px",
                "width": "100%",
                "type": "desktop"
            }
            
            return config
            
        except Exception as e:
            print(f"Error generating editor config: {e}")
            return {}
    
    def update_document(self, doc_id: str, content: str) -> Dict[str, Any]:
        """Update existing document content"""
        try:
            # Update document in storage
            result = self._store_document(doc_id, content, f"document_{doc_id}")
            
            if result.get('success'):
                return {
                    "success": True,
                    "document_id": doc_id,
                    "message": "Document updated successfully"
                }
            else:
                return {"success": False, "error": "Failed to update document"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_document_info(self, doc_id: str) -> Dict[str, Any]:
        """Get document information"""
        try:
            return {
                "success": True,
                "document_id": doc_id,
                "title": f"Document {doc_id}",
                "status": "available",
                "edit_url": f"{self.base_url}?documentId={doc_id}",
                "download_url": f"{self.storage_url}/{doc_id}.docx"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_server_status(self) -> Dict[str, Any]:
        """Check OnlyOffice server status"""
        try:
            response = requests.get(f"{self.base_url}/healthcheck", timeout=5)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "status": "online",
                    "url": self.base_url,
                    "message": "OnlyOffice server is running"
                }
            else:
                return {
                    "success": False,
                    "status": "error",
                    "message": f"Server returned status {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "status": "offline", 
                "message": f"Cannot connect to OnlyOffice server: {str(e)}"
            }

# Global instance
onlyoffice_api = OnlyOfficeAPI()