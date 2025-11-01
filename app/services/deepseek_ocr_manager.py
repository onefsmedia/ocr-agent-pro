"""
DeepSeek OCR Local Service Helper
Manages connection and communication with local DeepSeek OCR installation
"""

import subprocess
import time
import requests
import os
import json
from typing import Optional, Dict, Any
from flask import current_app

class DeepSeekOCRManager:
    """Manages local DeepSeek OCR service"""
    
    def __init__(self):
        self.deepseek_path = None
        self.deepseek_env = None
        self.server_process = None
        self.server_url = "http://localhost:8001"
        self.is_running = False
        
        # Get configuration
        try:
            if hasattr(current_app, 'config'):
                self.deepseek_path = current_app.config.get('DEEPSEEK_OCR_PATH')
                self.deepseek_env = current_app.config.get('DEEPSEEK_OCR_ENV')
                self.server_url = current_app.config.get('DEEPSEEK_OCR_URL', 'http://localhost:8001')
        except (RuntimeError, AttributeError):
            # Fallback when current_app is not available
            self.deepseek_path = r'D:\AIWORKS\DeepSeek-OCR\DeepSeek-OCR\DeepSeek-OCR-master\DeepSeek-OCR-vllm'
            self.deepseek_env = 'vllm_env'
    
    def check_server_status(self) -> bool:
        """Check if DeepSeek OCR server is running"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            self.is_running = response.status_code == 200
            return self.is_running
        except requests.exceptions.RequestException:
            self.is_running = False
            return False
    
    def start_server(self) -> bool:
        """Start the DeepSeek OCR server if not running"""
        
        if self.check_server_status():
            print("DeepSeek OCR server is already running")
            return True
        
        # In containerized deployment, try to start via API
        if self._is_containerized():
            return self._start_containerized_server()
        
        # Local development - check if path exists
        if not self.deepseek_path or not os.path.exists(self.deepseek_path):
            print(f"DeepSeek OCR path not found: {self.deepseek_path}")
            return False
        
        try:
            # Change to DeepSeek OCR directory
            os.chdir(self.deepseek_path)
            
            # Activate conda environment and start server
            if os.name == 'nt':  # Windows
                activate_cmd = f"conda activate {self.deepseek_env}"
                server_cmd = "python app.py"
                full_cmd = f'{activate_cmd} && {server_cmd}'
                
                # Start in background
                self.server_process = subprocess.Popen(
                    full_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:  # Linux/Mac
                activate_cmd = f"source activate {self.deepseek_env}"
                server_cmd = "python app.py"
                full_cmd = f"bash -c '{activate_cmd} && {server_cmd}'"
                
                self.server_process = subprocess.Popen(
                    full_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # Wait for server to start
            print("Starting DeepSeek OCR server...")
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self.check_server_status():
                    print("DeepSeek OCR server started successfully!")
                    return True
                print(f"Waiting for server... ({i+1}/30)")
            
            print("Failed to start DeepSeek OCR server")
            return False
            
        except Exception as e:
            print(f"Error starting DeepSeek OCR server: {e}")
            return False
    
    def stop_server(self):
        """Stop the DeepSeek OCR server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            self.is_running = False
            print("DeepSeek OCR server stopped")
    
    def _is_containerized(self) -> bool:
        """Check if running in containerized environment"""
        return os.getenv('CONTAINER_ENV') == 'true' or os.path.exists('/app/app.py')
    
    def _start_containerized_server(self) -> bool:
        """Start DeepSeek OCR server in containerized environment"""
        try:
            # In containerized setup, just check if the service is reachable
            # The actual server should be managed by Docker/Podman
            response = requests.get(f"{self.server_url}/health", timeout=10)
            if response.status_code == 200:
                print("DeepSeek OCR container service is available")
                return True
            else:
                print(f"DeepSeek OCR container service returned status: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error checking containerized DeepSeek OCR service: {e}")
            return False
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get information about the DeepSeek OCR server"""
        try:
            if self.check_server_status():
                response = requests.get(f"{self.server_url}/info", timeout=5)
                if response.status_code == 200:
                    return response.json()
        except requests.exceptions.RequestException:
            pass
        
        return {
            "status": "offline",
            "path": self.deepseek_path,
            "environment": self.deepseek_env,
            "url": self.server_url
        }
    
    def process_image_ocr(self, image_base64: str) -> Optional[str]:
        """Process image with DeepSeek OCR"""
        
        if not self.check_server_status():
            if not self.start_server():
                return None
        
        try:
            payload = {
                "image": image_base64,
                "format": "png",
                "options": {
                    "language": "auto",
                    "extract_tables": True,
                    "extract_equations": True,
                    "preserve_layout": True
                }
            }
            
            response = requests.post(
                f"{self.server_url}/api/ocr",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('text', '')
            else:
                print(f"DeepSeek OCR API error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"DeepSeek OCR request failed: {e}")
            return None

# Global instance
deepseek_manager = DeepSeekOCRManager()