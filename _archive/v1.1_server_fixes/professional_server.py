#!/usr/bin/env python3
"""
Professional Server Diagnostic Script
Comprehensive logging and error handling for production deployment
"""

import os
import sys
import time
import threading
import socket
import signal
import logging
from datetime import datetime

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('server_diagnostic.log')
    ]
)
logger = logging.getLogger(__name__)

def check_port_availability(host, port):
    """Check if port is available for binding"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result != 0  # True if port is free
    except Exception as e:
        logger.error(f"Port check failed: {e}")
        return False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

def main():
    """Main server startup with comprehensive diagnostics"""
    logger.info("=== OCR AGENT PRO SERVER DIAGNOSTIC ===")
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Working Directory: {os.getcwd()}")
    
    # Set working directory
    project_dir = r'c:\OCR Agent'
    os.chdir(project_dir)
    sys.path.insert(0, project_dir)
    logger.info(f"Changed to project directory: {project_dir}")
    
    # Check port availability
    host, port = '127.0.0.1', 5000
    if not check_port_availability(host, port):
        logger.error(f"Port {port} is already in use!")
        return False
    
    logger.info(f"Port {port} is available")
    
    try:
        # Test Flask app creation
        logger.info("Creating Flask application...")
        from app import create_app
        app = create_app()
        logger.info("✅ Flask app created successfully")
        
        # Test with Flask development server first
        logger.info("Testing Flask development server...")
        
        def run_flask_dev():
            try:
                app.run(
                    host=host,
                    port=port,
                    debug=False,
                    use_reloader=False,
                    threaded=True
                )
            except Exception as e:
                logger.error(f"Flask dev server error: {e}")
        
        # Start server in background thread for testing
        server_thread = threading.Thread(target=run_flask_dev, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Test connection
        import requests
        try:
            response = requests.get(f'http://{host}:{port}/api/health', timeout=5)
            logger.info(f"✅ Server responding: HTTP {response.status_code}")
            
            # Test main dashboard
            response = requests.get(f'http://{host}:{port}/', timeout=5)
            logger.info(f"✅ Dashboard responding: HTTP {response.status_code}")
            
            logger.info("🎉 SERVER IS WORKING! Starting permanent server...")
            
            # If tests pass, start the real server
            app.run(
                host='0.0.0.0',
                port=port,
                debug=False,
                use_reloader=False,
                threaded=True
            )
            
        except requests.exceptions.ConnectionError:
            logger.error("❌ Server not responding - connection refused")
            return False
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    success = main()
    if not success:
        logger.error("Server startup failed!")
        sys.exit(1)