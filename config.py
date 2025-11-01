import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://renderman:Master%402025@localhost:5432/ocr_agent'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max file size
    
    # OCR settings
    TESSERACT_PATH = os.environ.get('TESSERACT_PATH') or '/usr/bin/tesseract'
    USE_DEEPSEEK_OCR = os.environ.get('USE_DEEPSEEK_OCR', 'true').lower() == 'true'
    DEEPSEEK_OCR_URL = os.environ.get('DEEPSEEK_OCR_URL', 'http://localhost:8001')
    DEEPSEEK_OCR_PATH = os.environ.get('DEEPSEEK_OCR_PATH', r'D:\AIWORKS\DeepSeek-OCR\DeepSeek-OCR\DeepSeek-OCR-master\DeepSeek-OCR-vllm')
    DEEPSEEK_OCR_ENV = os.environ.get('DEEPSEEK_OCR_ENV', 'vllm_env')
    
    # OnlyOffice API settings
    ONLYOFFICE_URL = os.environ.get('ONLYOFFICE_URL', 'http://localhost:8000')
    ONLYOFFICE_SECRET = os.environ.get('ONLYOFFICE_SECRET', '')
    ONLYOFFICE_TOKEN = os.environ.get('ONLYOFFICE_TOKEN', '')
    ONLYOFFICE_STORAGE_URL = os.environ.get('ONLYOFFICE_STORAGE_URL', 'http://localhost:5000/storage')
    
    # AI/LLM settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL') or 'http://localhost:11434'
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL') or 'llama3.3:latest'
    LM_STUDIO_BASE_URL = os.environ.get('LM_STUDIO_BASE_URL') or 'http://localhost:1234'
    DEFAULT_LLM_PROVIDER = os.environ.get('DEFAULT_LLM_PROVIDER') or 'ollama'
    
    # Vector embedding settings
    EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL') or 'all-MiniLM-L6-v2'
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', '500'))
    CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', '50'))
    
    # Redis settings (for Celery)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # API settings
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT') or '100 per hour'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    
    # Large file handling settings
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year cache for static files
    MAX_CONTENT_PATH = None  # No path length limit
    
    # Extended timeouts for large file processing (increased for 500MB files)
    OCR_PROCESSING_TIMEOUT = 7200  # 2 hours for OCR processing (500MB files)
    CHUNK_PROCESSING_TIMEOUT = 1800  # 30 minutes for chunk processing
    UPLOAD_PROCESSING_TIMEOUT = 3600  # 1 hour for upload processing
    EMBEDDING_PROCESSING_TIMEOUT = 2400  # 40 minutes for embedding generation
    
    # Large file processing settings
    LARGE_FILE_CHUNK_SIZE = 1024 * 1024  # 1MB chunks for large file processing
    LARGE_FILE_THRESHOLD = 50 * 1024 * 1024  # 50MB threshold for large file handling
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class SQLiteFallbackConfig(Config):
    """SQLite fallback configuration for when PostgreSQL is not available"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ocr_agent.db'
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'sqlite': SQLiteFallbackConfig,
    'default': DevelopmentConfig
}