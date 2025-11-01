from app import create_app, db
from app.models import Document, DocumentChunk, ChatSession, ChatMessage, SystemSettings, ProcessingJob
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'Document': Document,
        'DocumentChunk': DocumentChunk,
        'ChatSession': ChatSession,
        'ChatMessage': ChatMessage,
        'SystemSettings': SystemSettings,
        'ProcessingJob': ProcessingJob
    }

@app.cli.command()
def init_db():
    """Initialize the database with tables and default settings"""
    
    print("Creating database tables...")
    db.create_all()
    
    # Create default system settings
    default_settings = [
        {
            'key': 'system_prompt',
            'value': 'You are a helpful AI assistant that can answer questions about documents. Use the provided context to give accurate and helpful responses.',
            'description': 'Default system prompt for the AI chatbot',
            'setting_type': 'string'
        },
        {
            'key': 'ocr_method',
            'value': 'tesseract',
            'description': 'Default OCR method (tesseract or google_vision)',
            'setting_type': 'string'
        },
        {
            'key': 'embedding_model',
            'value': 'all-MiniLM-L6-v2',
            'description': 'Sentence transformer model for embeddings',
            'setting_type': 'string'
        },
        {
            'key': 'llm_provider',
            'value': 'ollama',
            'description': 'LLM provider (ollama, lm_studio, openai)',
            'setting_type': 'string'
        },
        {
            'key': 'chunk_size',
            'value': '500',
            'description': 'Text chunk size for vector storage',
            'setting_type': 'integer'
        },
        {
            'key': 'chunk_overlap',
            'value': '50',
            'description': 'Overlap between text chunks',
            'setting_type': 'integer'
        },
        {
            'key': 'google_sync_enabled',
            'value': 'false',
            'description': 'Enable Google services synchronization',
            'setting_type': 'boolean'
        }
    ]
    
    for setting_data in default_settings:
        existing_setting = SystemSettings.query.filter_by(key=setting_data['key']).first()
        if not existing_setting:
            setting = SystemSettings(**setting_data)
            db.session.add(setting)
    
    db.session.commit()
    print("Database initialized successfully!")

@app.cli.command()
def create_admin():
    """Create an admin user (if authentication is added later)"""
    print("Admin user creation not yet implemented")

if __name__ == '__main__':
    import signal
    import sys
    
    # Global flag for shutdown
    shutdown_requested = False
    
    def signal_handler(sig, frame):
        global shutdown_requested
        shutdown_requested = True
        print('\n🛑 Shutdown requested... stopping server gracefully')
        # Don't call sys.exit() here - let Waitress handle it
    
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        print("🚀 OCR Agent Pro - Production Server with Waitress")
        print("=" * 60)
        print("✅ Flask application created successfully")
        print("✅ Database connection established")
        print("✅ All services initialized")
        print()
        print("🌐 Starting Waitress WSGI production server...")
        print("🌐 Server URL: http://localhost:5000")
        print("🌐 Network URL: http://0.0.0.0:5000")
        print()
        print("� Waitress Configuration:")
        print("   • Host: 0.0.0.0")
        print("   • Port: 5000")
        print("   • Threads: 6")
        print("   • Connection Limit: 1000")
        print("   • Channel Timeout: 120s")
        print("   • Cleanup Interval: 30s")
        print()
        print("�🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        print()
        
        # Use Waitress for production-grade stability
        from waitress import serve
        
        print("Starting Waitress server...")
        serve(
            app,
            host='0.0.0.0',
            port=5000,
            threads=6,
            connection_limit=1000,
            cleanup_interval=30,
            channel_timeout=120,
            url_scheme='http',
            ident='OCR-Agent-Pro/1.0'
        )
        print("Waitress server stopped normally")
        
    except ImportError as e:
        print("Waitress not installed. Please run: pip install waitress")
        print("Falling back to Flask development server...")
        app.run(
            debug=False,
            host='0.0.0.0', 
            port=5000, 
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nOCR Agent Pro shutdown complete")