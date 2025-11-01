#!/usr/bin/env python3
"""
OCR Agent Pro - Waitress Production Server
Professional WSGI server for production deployment
"""

import os
import sys
import signal
import time
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    missing_deps = []
    
    try:
        import waitress
        print("✅ Waitress WSGI server - Available")
    except ImportError:
        missing_deps.append("waitress")
    
    try:
        from app import create_app
        print("✅ Flask application - Available")
    except ImportError as e:
        print(f"❌ Flask application - Error: {e}")
        missing_deps.append("flask-app")
    
    try:
        import psycopg2
        print("✅ PostgreSQL driver - Available")
    except ImportError:
        missing_deps.append("psycopg2-binary")
    
    if missing_deps:
        print("\n❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\nInstall missing dependencies with:")
        print("pip install waitress psycopg2-binary")
        return False
    
    print("✅ All dependencies satisfied")
    return True

def test_database_connection():
    """Test database connectivity"""
    print("🔗 Testing database connection...")
    
    try:
        from app import create_app, db
        from app.models import Document
        
        app = create_app()
        with app.app_context():
            # Test basic query
            doc_count = Document.query.count()
            print(f"✅ Database connected successfully - {doc_count} documents")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   • Check if PostgreSQL is running")
        print("   • Verify database credentials in .env file")
        return False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print(f"\n🛑 Received signal {signum}")
    print("🔄 Initiating graceful shutdown...")
    sys.exit(0)

def create_flask_app():
    """Create and configure Flask application"""
    print("🚀 Creating Flask application...")
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return app
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        raise

def start_waitress_server(app):
    """Start Waitress WSGI server with optimal configuration"""
    print("🌐 Starting Waitress WSGI server...")
    
    try:
        from waitress import serve
        
        # Server configuration
        config = {
            'host': '0.0.0.0',
            'port': 5000,
            'threads': 6,
            'connection_limit': 1000,
            'cleanup_interval': 30,
            'channel_timeout': 120,
            'url_scheme': 'http',
            'ident': 'OCR-Agent-Pro/1.0',
            'clear_untrusted_proxy_headers': True
        }
        
        print("\n🔧 Waitress Configuration:")
        for key, value in config.items():
            print(f"   • {key}: {value}")
        
        print(f"\n🌐 Server URLs:")
        print(f"   • Local: http://localhost:5000")
        print(f"   • Network: http://0.0.0.0:5000")
        print(f"\n🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        # Start server
        serve(app, **config)
        
    except ImportError:
        print("❌ Waitress not installed!")
        print("Install with: pip install waitress")
        raise
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        raise

def main():
    """Main server startup function"""
    print("🚀 OCR Agent Pro - Waitress Production Server")
    print("=" * 60)
    print(f"🕒 Startup time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Step 1: Check dependencies
        if not check_dependencies():
            sys.exit(1)
        print()
        
        # Step 2: Test database
        if not test_database_connection():
            print("⚠️  Warning: Database connection failed")
            print("   Server will start but may have limited functionality")
        print()
        
        # Step 3: Create Flask app
        app = create_flask_app()
        print()
        
        # Step 4: Start Waitress server
        start_waitress_server(app)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("\n✅ OCR Agent Pro shutdown complete")

if __name__ == "__main__":
    main()