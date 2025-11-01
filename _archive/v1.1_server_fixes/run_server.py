#!/usr/bin/env python3
"""
Improved Flask App Starter with Connection Reliability
Fixes server connection issues and timeout problems
"""

from app import create_app, db
import os
import sys
import signal
import time
from threading import Thread
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FlaskAppManager:
    """Manages Flask app startup with reliability improvements"""
    
    def __init__(self):
        self.app = None
        self.running = False
        
    def create_app_with_retry(self, max_retries=3):
        """Create Flask app with retry logic"""
        for attempt in range(max_retries):
            try:
                logger.info(f"Creating Flask app (attempt {attempt + 1}/{max_retries})")
                self.app = create_app()
                
                # Test database connection
                with self.app.app_context():
                    db.session.execute(db.text('SELECT 1'))
                    logger.info("Database connection verified")
                
                logger.info("Flask app created successfully")
                return True
                
            except Exception as e:
                logger.error(f"App creation attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    logger.info("Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    logger.error("All app creation attempts failed")
                    return False
        
        return False
    
    def setup_signal_handlers(self):
        """Setup graceful shutdown handlers"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down gracefully...")
            self.running = False
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def run_server(self, host='0.0.0.0', port=5000, debug=True):
        """Run Flask server with improved configuration"""
        if not self.app:
            logger.error("No Flask app available")
            return False
        
        try:
            logger.info(f"Starting Flask server on {host}:{port}")
            self.running = True
            
            # Configure server settings for better reliability
            self.app.config.update({
                'SEND_FILE_MAX_AGE_DEFAULT': 0,  # Disable caching in debug mode
                'TEMPLATES_AUTO_RELOAD': True,
                'EXPLAIN_TEMPLATE_LOADING': False
            })
            
            # Run with specific settings to prevent common issues
            self.app.run(
                host=host,
                port=port,
                debug=debug,
                use_reloader=False,  # Prevent reloader issues
                use_debugger=debug,
                threaded=True,       # Enable threading for concurrent requests
                processes=1          # Single process to avoid database connection issues
            )
            
        except OSError as e:
            if "Address already in use" in str(e):
                logger.error(f"Port {port} is already in use")
                logger.info("Trying to kill existing processes...")
                self.kill_existing_processes(port)
                return False
            else:
                logger.error(f"Server startup failed: {e}")
                return False
        except Exception as e:
            logger.error(f"Unexpected error during server startup: {e}")
            return False
    
    def kill_existing_processes(self, port):
        """Kill processes using the specified port"""
        try:
            import subprocess
            
            # Find processes using the port
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    ['netstat', '-ano'], 
                    capture_output=True, 
                    text=True
                )
                lines = result.stdout.split('\\n')
                for line in lines:
                    if f':{port}' in line and 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) > 4:
                            pid = parts[-1]
                            logger.info(f"Killing process {pid} using port {port}")
                            subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
            else:  # Unix-like
                subprocess.run(['fuser', '-k', f'{port}/tcp'], capture_output=True)
                
        except Exception as e:
            logger.warning(f"Could not kill existing processes: {e}")
    
    def health_check(self):
        """Perform health check"""
        if not self.app:
            return False
        
        try:
            with self.app.app_context():
                # Test database
                db.session.execute(db.text('SELECT 1'))
                
                # Test OCR service
                from app.services.ocr_service import OCRService
                ocr_service = OCRService()
                languages = ocr_service.get_tesseract_languages()
                
                # Test embedding service
                from app.services.embedding_service import EmbeddingService
                embedding_service = EmbeddingService()
                
                logger.info("Health check passed")
                logger.info(f"OCR languages available: {languages}")
                return True
                
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

def main():
    """Main startup function"""
    logger.info("🚀 Starting OCR Agent Pro with improved reliability")
    
    # Create app manager
    manager = FlaskAppManager()
    
    # Setup signal handlers
    manager.setup_signal_handlers()
    
    # Create app with retry
    if not manager.create_app_with_retry():
        logger.error("❌ Failed to create Flask app")
        sys.exit(1)
    
    # Perform health check
    if not manager.health_check():
        logger.error("❌ Health check failed")
        sys.exit(1)
    
    # Start server
    logger.info("✅ All checks passed, starting server...")
    if not manager.run_server():
        logger.error("❌ Server startup failed")
        sys.exit(1)

if __name__ == '__main__':
    main()