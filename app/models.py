from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import UUID
# from pgvector.sqlalchemy import Vector  # Commented out for standard PostgreSQL
import uuid

class Document(db.Model):
    """Document model for storing uploaded files and OCR results"""
    __tablename__ = 'documents'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    
    # Document classification for Cameroonian education system
    document_type = db.Column(db.String(50))  # 'curriculum', 'textbook', 'progression'
    subject = db.Column(db.String(100))
    class_level = db.Column(db.String(50))
    
    # OCR results
    extracted_text = db.Column(db.Text)
    ocr_method = db.Column(db.String(50))  # 'tesseract' or 'deepseek_ocr'
    processing_status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    
    # OnlyOffice integration
    onlyoffice_file_id = db.Column(db.String(100))
    onlyoffice_sheet_id = db.Column(db.String(100))
    onlyoffice_doc_id = db.Column(db.String(100))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chunks = db.relationship('DocumentChunk', backref='document', lazy=True, cascade='all, delete-orphan')

class DocumentChunk(db.Model):
    """Text chunks for vector search and retrieval"""
    __tablename__ = 'document_chunks'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = db.Column(UUID(as_uuid=True), db.ForeignKey('documents.id'), nullable=False)
    
    # Chunk content
    content = db.Column(db.Text, nullable=False)
    chunk_index = db.Column(db.Integer, nullable=False)
    start_char = db.Column(db.Integer)
    end_char = db.Column(db.Integer)
    
    # Vector embedding (stored as JSON for now, can be migrated to pgvector later)
    embedding = db.Column(db.JSON)  # Will store embedding as JSON array
    
    # Chunk metadata
    chunk_metadata = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatSession(db.Model):
    """Chat sessions for the AI assistant"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_name = db.Column(db.String(255))
    system_prompt = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')

class ChatMessage(db.Model):
    """Individual chat messages"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = db.Column(UUID(as_uuid=True), db.ForeignKey('chat_sessions.id'), nullable=False)
    
    role = db.Column(db.String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = db.Column(db.Text, nullable=False)
    
    # Context and sources
    retrieved_chunks = db.Column(db.JSON)  # IDs of chunks used for RAG
    model_used = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemSettings(db.Model):
    """System configuration settings"""
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.Text)
    setting_type = db.Column(db.String(50))  # 'string', 'boolean', 'integer', 'json'
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProcessingJob(db.Model):
    """Background processing jobs tracking"""
    __tablename__ = 'processing_jobs'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_type = db.Column(db.String(50), nullable=False)  # 'ocr', 'embedding', 'sync'
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    
    # Job details
    document_id = db.Column(UUID(as_uuid=True), db.ForeignKey('documents.id'))
    progress = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
    result_data = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

class Subject(db.Model):
    """Subjects in the Cameroonian education system"""
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    name_french = db.Column(db.String(100))  # French translation
    category = db.Column(db.String(50))  # 'science', 'humanities', 'languages', 'arts', 'technical'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ClassLevel(db.Model):
    """Class levels in the Cameroonian education system"""
    __tablename__ = 'class_levels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    name_french = db.Column(db.String(50))  # French translation
    education_level = db.Column(db.String(30))  # 'primary', 'secondary_first_cycle', 'secondary_second_cycle'
    education_section = db.Column(db.String(20))  # 'english', 'french', 'both'
    grade_number = db.Column(db.Integer)  # For ordering
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)