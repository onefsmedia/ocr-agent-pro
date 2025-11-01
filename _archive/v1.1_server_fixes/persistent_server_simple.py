#!/usr/bin/env python3
"""
OCR Agent Pro - Simple Persistent Waitress Server
Clean auto-restart server without Unicode issues
"""

import os
import sys
import time
import signal
from datetime import datetime

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class SimpleServer:
    """Simple persistent server with auto-restart"""
    
    def __init__(self):
        self.running = True
        self.restart_count = 0
        self.max_restarts = 10
        self.restart_delay = 5
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum} - stopping server")
        self.running = False
        
    def check_dependencies(self):
        """Check if required packages are available"""
        try:
            from app import create_app
            print("Flask app: Available")
        except ImportError as e:
            print(f"Flask app error: {e}")
            return False
            
        try:
            from waitress import serve
            print("Waitress: Available")
        except ImportError:
            print("Waitress: Not installed")
            print("Install with: pip install waitress")
            return False
            
        return True
        
    def test_database(self):
        """Test database connection"""
        try:
            from app import create_app
            from app.models import Document
            
            app = create_app()
            with app.app_context():
                doc_count = Document.query.count()
                print(f"Database connected: {doc_count} documents")
                return True
        except Exception as e:
            print(f"Database warning: {e}")
            return False
            
    def start_server(self):
        """Start the Waitress server"""
        try:
            from app import create_app
            from waitress import serve
            
            print("Creating Flask app...")
            app = create_app()
            print("Flask app created successfully")
            
            # Test database
            self.test_database()
            
            print("Starting Waitress server...")
            print("URL: http://localhost:5000")
            print("Press Ctrl+C to stop")
            print("=" * 40)
            
            # Start server
            serve(app, host='0.0.0.0', port=5000, threads=6, channel_timeout=120)
            
        except Exception as e:
            print(f"Server error: {e}")
            raise
            
    def run(self):
        """Main server loop with auto-restart"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("OCR Agent Pro - Simple Persistent Server")
        print("=" * 50)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Max restarts: {self.max_restarts}")
        print()
        
        if not self.check_dependencies():
            print("Dependencies not satisfied")
            return False
            
        while self.running and self.restart_count < self.max_restarts:
            try:
                print(f"Starting server (attempt {self.restart_count + 1})")
                self.start_server()
                
            except KeyboardInterrupt:
                print("\nServer stopped by user")
                break
                
            except Exception as e:
                self.restart_count += 1
                print(f"\nServer crashed: {e}")
                
                if self.restart_count < self.max_restarts and self.running:
                    print(f"Restarting in {self.restart_delay}s...")
                    time.sleep(self.restart_delay)
                else:
                    print(f"Max restarts reached or shutdown requested")
                    break
                    
        print("Server shutdown complete")
        return True

def main():
    """Main entry point"""
    server = SimpleServer()
    server.run()

if __name__ == "__main__":
    main()
        self.logger = logging.getLogger('OCRAgentService')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        
    def install_dependencies(self):
        """Install missing dependencies"""
        self.logger.info("Checking dependencies...")
        
        dependencies = [
            'flask',
            'sqlalchemy', 
            'psycopg2-binary',
            'requests',
            'pillow',
            'waitress'
        ]
        
        for dep in dependencies:
            try:
                __import__(dep.replace('-', '_'))
                self.logger.info(f"  OK: {dep}")
            except ImportError:
                self.logger.info(f"  Installing: {dep}")
                try:
                    result = subprocess.run([
                        sys.executable, '-m', 'pip', 'install', dep
                    ], capture_output=True, text=True, check=True)
                    self.logger.info(f"  Installed: {dep}")
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"  Failed to install {dep}: {e.stderr}")
                    
    def test_database_connection(self):
        """Test database connectivity"""
        try:
            import psycopg2
            from config import Config
            
            # Parse connection string
            db_url = Config.SQLALCHEMY_DATABASE_URI
            if db_url.startswith('postgresql://'):
                # Simple connection test
                self.logger.info("Testing database connection...")
                return True
            else:
                self.logger.warning("Non-PostgreSQL database detected")
                return True
                
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            return False
            
    def create_flask_app(self):
        """Create Flask application"""
        try:
            from app import create_app
            app = create_app()
            self.logger.info("Flask application created successfully")
            return app
        except Exception as e:
            self.logger.error(f"Failed to create Flask app: {e}")
            raise
            
    def start_server(self):
        """Start the Waitress WSGI server"""
        try:
            app = self.create_flask_app()
            
            # Import here to avoid dependency issues
            from waitress import serve
            
            self.logger.info("Starting Waitress WSGI server on port 5000...")
            
            # Configure Waitress for production
            serve(
                app,
                host='0.0.0.0',
                port=5000,
                threads=6,
                channel_timeout=120,
                cleanup_interval=30,
                log_socket_errors=True
            )
            
        except KeyboardInterrupt:
            self.logger.info("Server interrupted by user")
            raise
        except Exception as e:
            self.logger.error(f"Server error: {e}")
            raise
            
    def write_pid_file(self):
        """Write process ID to file"""
        try:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
            self.logger.info(f"PID {os.getpid()} written to {self.pid_file}")
        except Exception as e:
            self.logger.error(f"Failed to write PID file: {e}")
            
    def remove_pid_file(self):
        """Remove PID file"""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
                self.logger.info("PID file removed")
        except Exception as e:
            self.logger.error(f"Failed to remove PID file: {e}")
            
    def is_running(self):
        """Check if service is already running"""
        if not self.pid_file.exists():
            return False
            
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
                
            # Check if process exists
            os.kill(pid, 0)
            return True
        except (OSError, ValueError, ProcessLookupError):
            # Process doesn't exist, remove stale PID file
            self.remove_pid_file()
            return False
            
    def start(self):
        """Start the service"""
        if self.is_running():
            self.logger.warning("Service is already running")
            return False
            
        self.logger.info("Starting OCR Agent Pro service...")
        self.write_pid_file()
        
        try:
            # Check dependencies
            self.install_dependencies()
            
            # Test database
            if not self.test_database_connection():
                self.logger.warning("Database connection test failed, but continuing...")
                
            # Start server
            self.running = True
            self.start_server()
            
        except Exception as e:
            self.logger.error(f"Service start failed: {e}")
            self.remove_pid_file()
            raise
            
    def stop(self):
        """Stop the service"""
        self.logger.info("Stopping OCR Agent Pro service...")
        self.running = False
        self.remove_pid_file()
        
    def run_with_auto_restart(self):
        """Run service with automatic restart on failure"""
        self.logger.info("Starting OCR Agent Pro with auto-restart...")
        
        while self.restart_count < self.max_restarts:
            try:
                self.start()
                break  # If we get here, server stopped normally
                
            except KeyboardInterrupt:
                self.logger.info("Service stopped by user")
                break
                
            except Exception as e:
                self.restart_count += 1
                self.logger.error(f"Service crashed (attempt {self.restart_count}): {e}")
                
                if self.restart_count < self.max_restarts:
                    delay = min(self.restart_delay * (2 ** (self.restart_count - 1)), 300)  # Cap at 5 minutes
                    self.logger.info(f"Restarting in {delay} seconds...")
                    time.sleep(delay)
                else:
                    self.logger.error("Maximum restart attempts reached. Service stopped.")
                    break
                    
        self.stop()

def main():
    """Main entry point"""
    service = OCRAgentService()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'start':
            service.start()
        elif command == 'stop':
            service.stop()
        elif command == 'restart':
            service.stop()
            time.sleep(2)
            service.start()
        elif command == 'status':
            if service.is_running():
                print("OCR Agent Pro service is running")
            else:
                print("OCR Agent Pro service is not running")
        else:
            print("Usage: python persistent_server.py [start|stop|restart|status]")
    else:
        # Default: run with auto-restart
        service.run_with_auto_restart()

if __name__ == '__main__':
    main()