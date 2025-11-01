"""
DeepSeek OCR Service API
Provides RESTful API interface to local DeepSeek OCR installation
"""

import os
import json
import base64
import subprocess
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from PIL import Image
import io
import tempfile

app = Flask(__name__)

# Configuration
DEEPSEEK_PATH = os.environ.get('DEEPSEEK_OCR_PATH', '/app/deepseek-ocr')
LOCAL_PATH = os.environ.get('DEEPSEEK_OCR_LOCAL_PATH', '')
CONDA_ENV = os.environ.get('CONDA_ENV', 'vllm_env')
HOST_IP = os.environ.get('HOST_IP', 'host.docker.internal')

class DeepSeekOCRService:
    def __init__(self):
        self.local_server_url = f"http://{HOST_IP}:8002"  # Assuming local server runs on 8002
        self.is_local_available = self.check_local_server()
    
    def check_local_server(self):
        """Check if local DeepSeek OCR server is running"""
        try:
            response = requests.get(f"{self.local_server_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_local_server(self):
        """Attempt to start local DeepSeek OCR server via host commands"""
        if self.is_local_available:
            return True
            
        try:
            # This would require host system access
            # For now, return instructions for manual start
            return False
        except Exception as e:
            print(f"Failed to start local server: {e}")
            return False
    
    def process_image(self, image_base64, options=None):
        """Process image with DeepSeek OCR"""
        
        # Try local server first
        if self.check_local_server():
            return self.process_with_local_server(image_base64, options)
        
        # Fallback to mock implementation for testing
        return self.process_with_mock(image_base64, options)
    
    def process_with_local_server(self, image_base64, options=None):
        """Process with actual local DeepSeek OCR server"""
        try:
            payload = {
                "image": image_base64,
                "format": "png",
                "options": options or {}
            }
            
            response = requests.post(
                f"{self.local_server_url}/api/ocr",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Local server error: {response.status_code}")
                
        except Exception as e:
            print(f"Local server processing failed: {e}")
            return None
    
    def process_with_mock(self, image_base64, options=None):
        """Mock processing for testing when local server unavailable"""
        try:
            # Decode image to verify it's valid
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # Mock OCR result
            mock_text = f"""DeepSeek OCR Mock Result
            
Image processed successfully at {datetime.now().isoformat()}
Image size: {image.size}
Format: {image.format}

This is a mock OCR result for testing purposes.
The actual text would be extracted by DeepSeek OCR from the image.

Advanced Features:
- Table extraction: {options.get('extract_tables', False)}
- Equation extraction: {options.get('extract_equations', False)}
- Layout preservation: {options.get('preserve_layout', True)}
- Language: {options.get('language', 'auto')}

To enable actual OCR processing, ensure your local DeepSeek OCR server 
is running at {self.local_server_url}
            """
            
            return {
                "text": mock_text,
                "confidence": 0.95,
                "processing_time": 2.5,
                "mode": "mock",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Mock processing failed: {e}")
            return None

# Initialize service
ocr_service = DeepSeekOCRService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "DeepSeek OCR API",
        "timestamp": datetime.now().isoformat(),
        "local_server_available": ocr_service.check_local_server(),
        "version": "1.0.0"
    })

@app.route('/info', methods=['GET'])
def get_info():
    """Get service information"""
    return jsonify({
        "service": "DeepSeek OCR Service",
        "version": "1.0.0",
        "deepseek_path": DEEPSEEK_PATH,
        "local_path": LOCAL_PATH,
        "conda_env": CONDA_ENV,
        "local_server_url": ocr_service.local_server_url,
        "local_server_status": "online" if ocr_service.check_local_server() else "offline",
        "capabilities": [
            "text_extraction",
            "table_extraction", 
            "equation_extraction",
            "layout_preservation",
            "multi_language"
        ]
    })

@app.route('/api/ocr', methods=['POST'])
def process_ocr():
    """Main OCR processing endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
        
        image_base64 = data['image']
        options = data.get('options', {})
        
        # Process with DeepSeek OCR
        result = ocr_service.process_image(image_base64, options)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "OCR processing failed"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/start-local', methods=['POST'])
def start_local_server():
    """Attempt to start local DeepSeek OCR server"""
    try:
        success = ocr_service.start_local_server()
        
        if success:
            return jsonify({
                "success": True,
                "message": "Local DeepSeek OCR server started successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to start local server. Please start manually.",
                "instructions": f"Run DeepSeek OCR server on {HOST_IP}:8002"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get detailed service status"""
    local_available = ocr_service.check_local_server()
    
    return jsonify({
        "service_status": "running",
        "local_server_available": local_available,
        "local_server_url": ocr_service.local_server_url,
        "deepseek_path": DEEPSEEK_PATH,
        "mode": "local" if local_available else "mock",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print(f"Starting DeepSeek OCR Service...")
    print(f"DeepSeek Path: {DEEPSEEK_PATH}")
    print(f"Local Path: {LOCAL_PATH}")
    print(f"Host IP: {HOST_IP}")
    print(f"Local server check: {ocr_service.check_local_server()}")
    
    app.run(host='0.0.0.0', port=8001, debug=False)