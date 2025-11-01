from flask import Blueprint, render_template, request, jsonify, current_app
from app.models import Document, DocumentChunk, SystemSettings, ChatSession
from app import db
import os
from sqlalchemy.exc import OperationalError

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    """Main dashboard with 6 panels"""
    
    try:
        # Get recent documents
        recent_documents = Document.query.order_by(Document.created_at.desc()).limit(5).all()
        
        # Get database stats
        doc_count = Document.query.count()
        chunk_count = DocumentChunk.query.count()
        
        # Get system settings
        settings = {s.key: s.value for s in SystemSettings.query.all()}
        
        # Get session count for dashboard stats
        session_count = ChatSession.query.count()
        
        database_status = 'connected'
        database_error = None
        
    except OperationalError as e:
        # Database connection failed - provide defaults
        recent_documents = []
        doc_count = 0
        chunk_count = 0
        session_count = 0
        settings = {}
        database_status = 'disconnected'
        database_error = str(e)
        current_app.logger.warning(f"Database connection failed: {e}")
    
    return render_template('dashboard.html', 
                         recent_documents=recent_documents,
                         doc_count=doc_count,
                         chunk_count=chunk_count,
                         session_count=session_count,
                         settings=settings,
                         database_status=database_status,
                         database_error=database_error)

@main_bp.route('/panel/ingestion')
def ingestion_panel():
    """Panel 1: Document ingestion form with enhanced UI"""
    return render_template('ingestion_standalone.html')

@main_bp.route('/panel/table')
def table_panel():
    """Panel 2: Table view of processed documents"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    documents = Document.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('panels/table.html', documents=documents)

@main_bp.route('/panel/settings')
def settings_panel():
    """Panel 3: System settings configuration with full GUI"""
    try:
        settings_dict = {s.key: s.value for s in SystemSettings.query.all()}
    except OperationalError:
        settings_dict = {}
    return render_template('settings_panel.html', settings=settings_dict)

@main_bp.route('/panel/database')
def database_panel():
    """Panel 4: Enhanced database status with real-time activity monitoring"""
    
    try:
        # Get all documents for the detailed table
        documents = Document.query.order_by(Document.updated_at.desc()).all()
        
        # Get database stats
        doc_count = Document.query.count()
        chunk_count = DocumentChunk.query.count()
        
        # Get system settings
        settings = {s.key: s.value for s in SystemSettings.query.all()}
        
        database_status = 'connected'
        database_error = None
        
    except OperationalError as e:
        documents = []
        doc_count = 0
        chunk_count = 0
        settings = {}
        database_status = 'disconnected'
        database_error = str(e)
    
    return render_template('database_panel.html', 
                         documents=documents,
                         doc_count=doc_count,
                         chunk_count=chunk_count,
                         database_status=database_status,
                         database_error=database_error,
                         settings=settings)

@main_bp.route('/panel/chatbot')
def chatbot_panel():
    """Panel 5: AI chatbot interface"""
    try:
        sessions = ChatSession.query.order_by(ChatSession.updated_at.desc()).all()
    except OperationalError as e:
        current_app.logger.warning(f"Database connection failed in chatbot panel: {e}")
        sessions = []
    except Exception as e:
        current_app.logger.error(f"Error loading chat sessions: {e}")
        sessions = []
    return render_template('panels/chatbot.html', sessions=sessions)

@main_bp.route('/panel/prompt')
def prompt_panel():
    """Panel 6: Prompt configuration"""
    # Get current system prompt from settings
    system_prompt_setting = SystemSettings.query.filter_by(key='system_prompt').first()
    current_prompt = system_prompt_setting.value if system_prompt_setting else ""
    
    return render_template('panels/prompt.html', current_prompt=current_prompt)

@main_bp.route('/panel/lesson-generator')
def lesson_generator_panel():
    """Panel 7: Lesson note generator with OnlyOffice integration"""
    return render_template('lesson_generator_panel.html')

@main_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'upload_dir': os.path.exists(current_app.config['UPLOAD_FOLDER'])
    })