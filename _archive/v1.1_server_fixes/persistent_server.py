"""
OCR Agent Pro - Persistent Background Service
Production-ready server with auto-restart and background operation
"""

import os
import sys
import time
import signal
import logging
import subprocess
from pathlib import Path
from datetime import datetime

class OCRAgentService:
    """Persistent background service for OCR Agent Pro"""
    
    def __init__(self):
        self.project_dir = Path(r'c:\OCR Agent')
        self.log_dir = self.project_dir / 'logs'
        self.pid_file = self.project_dir / 'ocr_agent.pid'
        self.restart_count = 0
        self.max_restarts = 10
        self.running = True
        
        # Ensure directories exist
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_file = self.log_dir / f"ocr_agent_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('OCRAgentService')
        
    def install_dependencies(self):
        """Install missing dependencies"""
        self.logger.info("🔧 Checking and installing dependencies...")
        
        dependencies = [
            'flask',
            'sqlalchemy', 
            'psycopg2-binary',
            'requests',
            'pillow',
            'sentence-transformers',
            'pytesseract',
            'pdf2image',
            'pypdf2',
            'watchdog',
            'waitress'
        ]
        
        for dep in dependencies:
            try:
                __import__(dep.replace('-', '_'))
                self.logger.info(f"   ✅ {dep} already installed")
            except ImportError:
                self.logger.info(f"   📦 Installing {dep}...")
                try:
                    subprocess.check_call([
                        sys.executable, '-m', 'pip', 'install', dep
                    ], capture_output=True)
                    self.logger.info(f"   ✅ {dep} installed successfully")
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"   ❌ Failed to install {dep}: {e}")
                    
    def create_flask_app(self):
        """Create and configure Flask application"""
        try:
            # Set working directory and path
            os.chdir(self.project_dir)
            if str(self.project_dir) not in sys.path:
                sys.path.insert(0, str(self.project_dir))
            
            # Import and create app
            from app import create_app
            from sqlalchemy import text
            
            app = create_app()
            
            # Test database connection
            with app.app_context():
                from app import db
                db.session.execute(text('SELECT 1'))
                self.logger.info("✅ Database connection verified")
            
            self.logger.info("✅ Flask application created successfully")
            return app
            
        except Exception as e:
            self.logger.error(f"❌ Flask app creation failed: {e}")
            raise
    
    def write_pid_file(self):
        """Write process ID to file"""
        try:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
            self.logger.info(f"📝 PID file written: {self.pid_file}")
        except Exception as e:
            self.logger.error(f"❌ Failed to write PID file: {e}")
    
    def cleanup_pid_file(self):
        """Remove PID file"""
        try:
            if self.pid_file.exists():
                self.pid_file.unlink()
                self.logger.info("🧹 PID file cleaned up")
        except Exception as e:
            self.logger.error(f"❌ Failed to cleanup PID file: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"📡 Received signal {signum}, shutting down gracefully...")
        self.running = False
        self.cleanup_pid_file()
    
    def start_server(self):
        """Start the Flask server with Waitress (production WSGI server)"""
        try:
            app = self.create_flask_app()
            
            # Use Waitress for production-grade serving
            from waitress import serve
            
            self.logger.info("🚀 Starting OCR Agent Pro server...")
            self.logger.info("🌐 Server URL: http://localhost:5000")
            self.logger.info("🔒 Production mode: Waitress WSGI server")
            
            # Serve with Waitress (much more stable than Flask dev server)
            serve(
                app,
                host='0.0.0.0',
                port=5000,
                threads=6,
                connection_limit=100,
                cleanup_interval=30,
                channel_timeout=120,
                log_untrusted_proxy_headers=True
            )
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Server stopped by user")
            self.running = False
        except Exception as e:
            self.logger.error(f"❌ Server error: {e}")
            raise
    
    def run_with_auto_restart(self):
        """Run server with automatic restart on failure"""
        self.logger.info("🔄 Starting OCR Agent Pro with auto-restart...")
        
        # Install signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Write PID file
        self.write_pid_file()
        
        while self.running and self.restart_count < self.max_restarts:
            try:
                self.install_dependencies()
                self.start_server()
                
                if self.running:  # If we exit cleanly, don't restart
                    break
                    
            except Exception as e:
                self.restart_count += 1
                self.logger.error(f"💥 Server crashed (restart #{self.restart_count}): {e}")
                
                if self.restart_count < self.max_restarts:
                    wait_time = min(30, 5 * self.restart_count)  # Exponential backoff
                    self.logger.info(f"⏰ Waiting {wait_time} seconds before restart...")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"💀 Max restarts ({self.max_restarts}) reached. Giving up.")
                    break
        
        self.cleanup_pid_file()
        self.logger.info("🏁 OCR Agent Pro service stopped")

def main():
    """Main entry point"""
    print("OCR Agent Pro - Persistent Background Service")
    print("=" * 50)
    
    service = OCRAgentService()
    
    # Check if already running
    if service.pid_file.exists():
        try:
            with open(service.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process is actually running
            try:
                os.kill(pid, 0)  # This doesn't kill, just checks if process exists
                print(f"⚠️  OCR Agent Pro is already running (PID: {pid})")
                print(f"   PID file: {service.pid_file}")
                print("   Use 'taskkill /PID {pid} /F' to stop it")
                return
            except OSError:
                # Process not running, remove stale PID file
                service.pid_file.unlink()
                print("🧹 Removed stale PID file")
        except (ValueError, FileNotFoundError):
            # Invalid or missing PID file
            pass
    
    try:
        service.run_with_auto_restart()
    except KeyboardInterrupt:
        print("\n🛑 Service stopped by user")
    except Exception as e:
        print(f"💥 Service failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())