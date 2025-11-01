"""
Large File Upload Service
Handles file uploads up to 500MB with progress tracking and chunked processing
"""

import os
import hashlib
import mimetypes
from werkzeug.utils import secure_filename
from flask import current_app, request
import uuid
from datetime import datetime

class LargeFileUploadService:
    """Service for handling large file uploads"""
    
    def __init__(self):
        self.max_file_size = 500 * 1024 * 1024  # 500MB
        self.allowed_extensions = {
            'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif', 
            'txt', 'doc', 'docx', 'rtf'
        }
    
    def validate_file(self, file):
        """Validate uploaded file"""
        errors = []
        
        if not file:
            errors.append("No file provided")
            return errors
        
        if file.filename == '':
            errors.append("No file selected")
            return errors
        
        # Check file extension
        if not self._allowed_file(file.filename):
            errors.append(f"File type not supported. Allowed: {', '.join(self.allowed_extensions)}")
        
        # Check file size (if available)
        if hasattr(file, 'content_length') and file.content_length:
            if file.content_length > self.max_file_size:
                size_mb = file.content_length / (1024 * 1024)
                max_mb = self.max_file_size / (1024 * 1024)
                errors.append(f"File too large: {size_mb:.1f}MB (max: {max_mb}MB)")
        
        return errors
    
    def _allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def save_file(self, file, upload_folder):
        """Save uploaded file with unique name"""
        try:
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_id = str(uuid.uuid4())
            name, ext = os.path.splitext(filename)
            unique_filename = f"{unique_id}_{name}{ext}"
            
            file_path = os.path.join(upload_folder, unique_filename)
            
            # Ensure upload directory exists
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save file
            file.save(file_path)
            
            # Get file info
            file_info = {
                'original_name': filename,
                'saved_name': unique_filename,
                'file_path': file_path,
                'file_size': os.path.getsize(file_path),
                'mime_type': mimetypes.guess_type(filename)[0],
                'upload_time': datetime.utcnow(),
                'file_hash': self._calculate_file_hash(file_path)
            }
            
            return file_info, None
            
        except Exception as e:
            return None, str(e)
    
    def _calculate_file_hash(self, file_path):
        """Calculate SHA256 hash of file"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except:
            return None
    
    def check_disk_space(self, upload_folder, required_space=None):
        """Check available disk space"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(upload_folder)
            
            if required_space:
                return free >= required_space
            
            return {
                'total_gb': total / (1024**3),
                'used_gb': used / (1024**3),
                'free_gb': free / (1024**3),
                'sufficient': free >= (2 * 1024**3)  # At least 2GB free
            }
        except:
            return False
    
    def estimate_processing_time(self, file_size_mb):
        """Estimate OCR processing time based on file size"""
        # Rough estimates based on file size
        if file_size_mb < 1:
            return "< 1 minute"
        elif file_size_mb < 10:
            return f"{int(file_size_mb * 0.5)} - {int(file_size_mb * 1)} minutes"
        elif file_size_mb < 50:
            return f"{int(file_size_mb * 0.3)} - {int(file_size_mb * 0.6)} minutes"
        else:
            return f"{int(file_size_mb * 0.2)} - {int(file_size_mb * 0.4)} minutes"
