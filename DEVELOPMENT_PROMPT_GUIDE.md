# Development Prompt Guide - Local Server Architecture

**Version:** 1.0  
**Last Updated:** November 2, 2025  
**Based on:** OCR Agent Pro v1.3.0  
**Repository Example:** https://github.com/onefsmedia/ocr-agent-pro

---

## 🎯 Purpose

This guide provides proven prompts and architectural patterns for developing applications with:
- **Local server infrastructure** (no cloud dependency)
- **Modular configuration** (modify without touching code)
- **Self-contained deployment** (runs on single machine or VM)
- **Extensible architecture** (add features without breaking existing functionality)

Use these prompts with AI assistants (GitHub Copilot, ChatGPT, Claude) or as requirements for your development team.

---

## 📋 Table of Contents

1. [Core Architecture Prompt](#core-architecture-prompt)
2. [Local Server Requirements Prompt](#local-server-requirements-prompt)
3. [Configuration-Driven Design Prompt](#configuration-driven-design-prompt)
4. [Database Setup Prompt](#database-setup-prompt)
5. [Modular Service Architecture Prompt](#modular-service-architecture-prompt)
6. [Deployment Flexibility Prompt](#deployment-flexibility-prompt)
7. [AI/LLM Integration Prompt](#aillm-integration-prompt)
8. [Security & Environment Prompt](#security--environment-prompt)
9. [Testing & Verification Prompt](#testing--verification-prompt)
10. [Documentation Standards Prompt](#documentation-standards-prompt)

---

## 1. Core Architecture Prompt

### 📝 Copy-Paste Prompt:

```
Create a production-ready web application with the following architecture:

FRAMEWORK & STACK:
- Backend: Flask 3.0+ with application factory pattern
- Database: PostgreSQL 12+ with extensions support
- Server: Waitress or Gunicorn WSGI for production
- Configuration: Environment-based (.env files)
- Deployment: Docker/Podman containers + native installation options

DESIGN PRINCIPLES:
1. Separation of concerns (routes, services, models in separate modules)
2. Configuration over code (all settings via .env, no hardcoded values)
3. Local-first architecture (runs completely offline if needed)
4. Modular services (each feature as independent service class)
5. Multiple deployment paths (Docker, VM, Windows, Linux)

PROJECT STRUCTURE:
app/
├── __init__.py          # Application factory
├── models.py            # Database models
├── routes/              # HTTP endpoints
├── services/            # Business logic
└── api/                 # API endpoints

scripts/
├── deployment/          # Deployment automation
├── setup/               # Initial setup scripts
├── configuration/       # Runtime configuration tools
└── maintenance/         # Diagnostic utilities

REQUIREMENTS:
- All external services (database, cache, LLM) configurable via .env
- Health check endpoints for monitoring
- Graceful degradation when optional services unavailable
- Comprehensive error handling and logging
- Database migrations support
- Development and production configurations
```

---

## 2. Local Server Requirements Prompt

### 📝 Copy-Paste Prompt:

```
Design the application to run entirely on local infrastructure with these requirements:

LOCAL SERVER COMPONENTS:
1. Web Application Server
   - Host: 0.0.0.0 (all interfaces) or 127.0.0.1 (localhost only)
   - Port: Configurable via environment variable (default 5000)
   - Protocol: HTTP (with optional HTTPS via reverse proxy)
   - Threads/Workers: Configurable based on CPU cores

2. Database Server (PostgreSQL)
   - Local installation or Docker container
   - Connection via localhost or Unix socket
   - Database name, user, password via .env
   - Support for extensions (pgvector, uuid-ossp, etc.)
   - Connection pooling configured

3. Cache/Queue Server (Redis) - Optional
   - Local Redis instance
   - Fallback to in-memory cache if unavailable
   - Connection via localhost
   - Password-protected

4. Document Processing Services
   - Tesseract OCR (local binary)
   - PDF processing (poppler-utils)
   - Image processing (PIL/Pillow)
   - All binaries path-configurable

5. AI/LLM Services - All Local Options
   - Ollama (localhost:11434)
   - LM Studio (localhost:1234)
   - Or fallback to OpenAI API (optional cloud)
   - Model paths configurable

CONFIGURATION REQUIREMENTS:
- All service URLs/paths in .env file
- Automatic service detection on startup
- Graceful handling of unavailable services
- Clear error messages for missing dependencies
- Health check endpoint shows all service statuses

NETWORK REQUIREMENTS:
- No internet required for core functionality
- Internet optional for: model downloads, API services, updates
- All ports configurable
- Firewall-friendly (minimal ports needed)
- Support for reverse proxy (NGINX/Apache)

RESOURCE REQUIREMENTS:
- Minimum specs clearly documented
- Recommended specs for production
- Resource usage monitoring
- Configurable memory limits
- Disk space requirements
```

---

## 3. Configuration-Driven Design Prompt

### 📝 Copy-Paste Prompt:

```
Implement a configuration-driven architecture where ALL behavior can be modified via configuration files without touching the codebase:

CONFIGURATION STRUCTURE:

1. Environment Variables (.env file):
   - Application settings (DEBUG, SECRET_KEY, FLASK_ENV)
   - Database connection (DATABASE_URL, POOL_SIZE)
   - Service URLs (REDIS_URL, OLLAMA_BASE_URL)
   - Feature flags (USE_DEEPSEEK_OCR, ENABLE_ONLYOFFICE)
   - File paths (UPLOAD_FOLDER, STORAGE_PATH, TESSERACT_PATH)
   - API keys (OPENAI_API_KEY, etc.)
   - Performance tuning (CHUNK_SIZE, MAX_WORKERS)

2. Config Class (config.py):
   - Load from environment with sensible defaults
   - Type conversion (strings to int, bool, paths)
   - Validation on startup
   - Different configs: Development, Testing, Production
   - Config.from_object() pattern

3. Service Configuration:
   - Each service reads config in __init__
   - No hardcoded values in service classes
   - Dependency injection pattern
   - Easy to swap implementations via config

MODULAR FEATURE SYSTEM:

Create features that can be enabled/disabled via configuration:

Example .env flags:
```
# Feature toggles
ENABLE_OCR=true
ENABLE_CHATBOT=true
ENABLE_ONLYOFFICE=false
ENABLE_VECTOR_SEARCH=true

# Provider selection (choose implementation)
LLM_PROVIDER=ollama  # Options: ollama, lm_studio, openai
OCR_ENGINE=tesseract  # Options: tesseract, deepseek
DATABASE_TYPE=postgresql  # Options: postgresql, sqlite

# Service endpoints (change without code modification)
OLLAMA_BASE_URL=http://localhost:11434
LM_STUDIO_BASE_URL=http://localhost:1234
ONLYOFFICE_URL=http://localhost:8080
```

IMPLEMENTATION PATTERN:

1. Service Factory Pattern:
```python
def create_llm_service(config):
    provider = config.get('LLM_PROVIDER', 'ollama')
    if provider == 'ollama':
        return OllamaService(config.OLLAMA_BASE_URL)
    elif provider == 'lm_studio':
        return LMStudioService(config.LM_STUDIO_BASE_URL)
    elif provider == 'openai':
        return OpenAIService(config.OPENAI_API_KEY)
    else:
        return None  # Graceful fallback
```

2. Feature Flag Decorator:
```python
def requires_feature(feature_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_app.config.get(f'ENABLE_{feature_name}', False):
                return jsonify({'error': f'{feature_name} disabled'}), 503
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

3. Dynamic Service Loading:
- Services check if dependencies available on startup
- Register themselves only if configured
- Routes disabled if service unavailable
- Clear logging of what's enabled/disabled

CONFIGURATION FILES:
- .env.example (template with all variables documented)
- .env.development (local dev settings)
- .env.production (production template)
- .env.test (testing configuration)

VALIDATION:
- Check required variables on startup
- Fail fast with clear error messages
- Provide hints for missing configuration
- Log all loaded configuration (sanitize secrets)
```

---

## 4. Database Setup Prompt

### 📝 Copy-Paste Prompt:

```
Create a database setup that supports local PostgreSQL installation with these features:

DATABASE ARCHITECTURE:

1. PostgreSQL with Extensions:
   - pgvector (for vector embeddings)
   - uuid-ossp (for UUID generation)
   - pg_trgm (for text search)
   
2. Connection Management:
   - SQLAlchemy ORM with connection pooling
   - Connection string via DATABASE_URL environment variable
   - Format: postgresql://user:password@host:port/database
   - Pool size configurable (default 20)
   - Max overflow configurable (default 40)
   - Connection timeout handling

3. Database Initialization:
   - Automated setup script (scripts/setup/setup_database.py)
   - Check if database exists
   - Create database if needed
   - Install required extensions
   - Run initial migrations
   - Seed data if specified

4. Migration System:
   - Flask-Migrate / Alembic for migrations
   - Migrations in version control
   - Upgrade/downgrade support
   - Migration script: python scripts/setup/migrate_database.py

5. Models Structure:
   - Base model with common fields (id, created_at, updated_at)
   - Mixin classes for common functionality
   - Relationships properly defined
   - Indexes for performance
   - Vector fields for embeddings (if using pgvector)

SETUP SCRIPT REQUIREMENTS:

```python
# scripts/setup/setup_database.py should:
1. Read DATABASE_URL from .env
2. Parse connection details
3. Connect to PostgreSQL server (without database)
4. Check if target database exists
5. Create database if missing
6. Connect to target database
7. Install extensions (CREATE EXTENSION IF NOT EXISTS)
8. Run Flask-Migrate upgrade
9. Verify tables created
10. Print status report
```

DOCKER SUPPORT:
- Docker Compose service for PostgreSQL
- Named volumes for data persistence
- Health check for container
- Init scripts for automatic setup
- Expose port 5432 (configurable)

BACKUP & RESTORE:
- Backup script using pg_dump
- Restore script using pg_restore
- Automated daily backups (cron/scheduled task)
- Backup location configurable

DATABASE STATUS ENDPOINT:
- API endpoint to check database health
- Show connection pool stats
- Display table counts
- Vector index status (if applicable)
```

---

## 5. Modular Service Architecture Prompt

### 📝 Copy-Paste Prompt:

```
Design a modular service layer where each major feature is an independent, swappable service:

SERVICE PATTERN:

1. Base Service Class:
```python
class BaseService:
    """Base class for all services"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._initialized = False
    
    def initialize(self):
        """Override to perform service initialization"""
        raise NotImplementedError
    
    def health_check(self):
        """Return service health status"""
        return {'status': 'unknown', 'initialized': self._initialized}
    
    def shutdown(self):
        """Clean up resources"""
        pass
```

2. Service Directory Structure:
```
app/services/
├── __init__.py              # Service registry
├── base_service.py          # Base service class
├── ocr_service.py           # Document OCR processing
├── embedding_service.py     # Text embeddings
├── llm_service.py           # LLM integration
├── onlyoffice_service.py    # Document editing
├── storage_service.py       # File storage
└── search_service.py        # Vector search
```

3. Service Requirements:
   - Each service in separate file
   - Clear interface/contract
   - Dependency injection via __init__
   - Configuration from config object
   - Error handling with proper exceptions
   - Logging for debugging
   - Health check method
   - Graceful degradation if dependencies missing

4. Service Registry Pattern:
```python
# app/services/__init__.py
class ServiceRegistry:
    _services = {}
    
    @classmethod
    def register(cls, name, service_class):
        cls._services[name] = service_class
    
    @classmethod
    def get(cls, name):
        return cls._services.get(name)
    
    @classmethod
    def initialize_all(cls, app):
        for name, service_class in cls._services.items():
            try:
                service = service_class(app.config)
                service.initialize()
                app.extensions[name] = service
                app.logger.info(f"✅ {name} service initialized")
            except Exception as e:
                app.logger.warning(f"⚠️ {name} service unavailable: {e}")
```

5. Service Examples:

OCR Service:
- Support multiple OCR engines (Tesseract, DeepSeek)
- Engine selection via config
- File format detection
- Language support configurable
- Batch processing support

LLM Service:
- Support multiple providers (Ollama, LM Studio, OpenAI)
- Provider switching via config
- Prompt templates
- Context management
- Streaming support

Embedding Service:
- Multiple embedding models
- Sentence Transformers integration
- Batch embedding generation
- Caching support
- Dimension validation

ADDING NEW SERVICES:

To add a new service without modifying existing code:
1. Create new file in app/services/
2. Inherit from BaseService
3. Implement required methods
4. Register in __init__.py
5. Add configuration to .env
6. Service auto-loads if config present

TESTING SERVICES:
- Unit tests for each service
- Mock external dependencies
- Test configuration variants
- Health check testing
- Error handling tests
```

---

## 6. Deployment Flexibility Prompt

### 📝 Copy-Paste Prompt:

```
Create multiple deployment options to support various infrastructure scenarios:

DEPLOYMENT OPTION 1: Docker Compose (Recommended)

Requirements:
- docker-compose.yml with all services
- Multi-service orchestration: app, database, redis, auxiliary services
- Named volumes for data persistence
- Health checks for all services
- Environment variable passthrough
- Service dependencies (depends_on with conditions)
- Network isolation
- Port mapping configurable

Services to include:
```yaml
services:
  postgres:    # PostgreSQL with pgvector
  redis:       # Cache and queue
  app:         # Main application
  celery:      # Background workers (if needed)
  nginx:       # Reverse proxy (optional)
  [auxiliary]: # Additional services (OnlyOffice, Ollama, etc.)
```

DEPLOYMENT OPTION 2: Native VM Installation

Requirements:
- Installation script for Ubuntu/Debian
- Installation script for CentOS/RHEL
- Installation script for Windows Server
- Dependency installation automated
- Virtual environment setup
- Database setup automated
- Systemd service file (Linux)
- Windows Service support (Windows)

DEPLOYMENT OPTION 3: Systemd Service (Linux Production)

Create service file template:
```ini
[Unit]
Description=Your Application Name
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=app_user
Group=app_user
WorkingDirectory=/opt/your-app
Environment="PATH=/opt/your-app/.venv/bin"
ExecStart=/opt/your-app/.venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

DEPLOYMENT OPTION 4: Container Image

Dockerfile requirements:
- Multi-stage build for smaller images
- Security: non-root user
- Health check built-in
- Configurable via environment variables
- All dependencies included
- Minimal base image (python:3.11-slim)
- Clear CMD/ENTRYPOINT
- Version tags

DEPLOYMENT SCRIPTS:

Create automated deployment scripts:
- scripts/deployment/deploy-docker.sh (Docker setup)
- scripts/deployment/deploy-vm.sh (VM installation)
- scripts/deployment/deploy-windows.ps1 (Windows setup)
- scripts/deployment/install-postgresql.sh (Database setup)

Each script should:
1. Check prerequisites
2. Install dependencies
3. Create necessary directories
4. Set up configuration files
5. Initialize database
6. Start services
7. Verify installation
8. Print access URLs

CONFIGURATION FLEXIBILITY:

Support multiple configuration methods:
- Environment variables (.env file)
- Command-line arguments
- Configuration file (config.yaml)
- Environment detection (dev/staging/prod)

DEPLOYMENT DOCUMENTATION:

Create comprehensive guides:
- DEPLOYMENT_GUIDE.md (all options)
- QUICKSTART.md (fastest path)
- DOCKER_DEPLOYMENT.md (container-specific)
- VM_DEPLOYMENT.md (native installation)
- DEVOPS_CHECKLIST.md (production checklist)

ROLLBACK SUPPORT:
- Version tagging in Git
- Database migration rollback
- Configuration backup
- Docker image versioning
- Clear rollback procedures documented
```

---

## 7. AI/LLM Integration Prompt

### 📝 Copy-Paste Prompt:

```
Integrate AI/LLM capabilities with support for multiple local and cloud providers:

LLM PROVIDER ARCHITECTURE:

1. Provider Abstraction:
   - Common interface for all LLM providers
   - Provider selection via configuration
   - Automatic fallback to available provider
   - Rate limiting and retry logic

2. Supported Providers:
   
   LOCAL PROVIDERS (No Internet Required):
   - Ollama (localhost:11434)
     * Model: llama3.3, mistral, etc.
     * Automatic model detection
     * Streaming support
   
   - LM Studio (localhost:1234)
     * OpenAI-compatible API
     * Model loaded via LM Studio UI
     * Context window configuration
   
   - vLLM (localhost:8000)
     * High-performance inference
     * Batch processing
     * Model path configurable

   CLOUD PROVIDERS (Requires Internet):
   - OpenAI (GPT-4, GPT-3.5)
   - Anthropic Claude
   - Google Gemini
   - Azure OpenAI

3. Configuration (.env):
```
# LLM Provider Selection
DEFAULT_LLM_PROVIDER=ollama  # ollama, lm_studio, openai, claude

# Local Providers
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.3:latest
LM_STUDIO_BASE_URL=http://localhost:1234
LM_STUDIO_MODEL=local-model

# Cloud Providers (Optional)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-opus

# LLM Parameters
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
LLM_TOP_P=0.9
```

4. LLM Service Implementation:

```python
class LLMService(BaseService):
    def __init__(self, config):
        super().__init__(config)
        self.provider = self._initialize_provider()
    
    def _initialize_provider(self):
        provider_name = self.config.get('DEFAULT_LLM_PROVIDER')
        
        if provider_name == 'ollama':
            return OllamaProvider(self.config)
        elif provider_name == 'lm_studio':
            return LMStudioProvider(self.config)
        elif provider_name == 'openai':
            return OpenAIProvider(self.config)
        # ... more providers
    
    def generate(self, prompt, **kwargs):
        """Generate response from LLM"""
        return self.provider.generate(prompt, **kwargs)
    
    def stream_generate(self, prompt, **kwargs):
        """Stream response from LLM"""
        return self.provider.stream_generate(prompt, **kwargs)
```

RAG (Retrieval-Augmented Generation) PATTERN:

1. Vector Embeddings:
   - Sentence Transformers (local)
   - Model: all-MiniLM-L6-v2 (384 dimensions)
   - Store embeddings in PostgreSQL with pgvector
   - Fast similarity search

2. Document Chunking:
   - Configurable chunk size (default 500 chars)
   - Overlap for context (default 50 chars)
   - Metadata preservation
   - Chunk relevance scoring

3. RAG Pipeline:
```
User Query → Embed Query → Vector Search → Top-K Results → 
Context Assembly → LLM Prompt → Generate Response
```

4. RAG Configuration:
```
# Vector Search Settings
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=50
VECTOR_SEARCH_TOP_K=5
SIMILARITY_THRESHOLD=0.7

# RAG Settings
RAG_ENABLE=true
RAG_CONTEXT_SIZE=3000  # Max chars for context
RAG_INCLUDE_METADATA=true
```

CHATBOT FEATURES:

1. Session Management:
   - Store conversation history
   - Context window management
   - Session persistence (database or Redis)
   - Session expiration configurable

2. Prompt Templates:
   - System prompts configurable
   - User prompt templates
   - Few-shot examples
   - Role-based prompts

3. Response Features:
   - Streaming responses (real-time)
   - Citation of sources (RAG)
   - Token usage tracking
   - Response caching

4. Safety Features:
   - Content filtering
   - Rate limiting per user
   - Input validation
   - Output sanitization

LLM TESTING:
- Mock LLM responses for testing
- Test prompt templates
- RAG accuracy testing
- Performance benchmarks
```

---

## 8. Security & Environment Prompt

### 📝 Copy-Paste Prompt:

```
Implement comprehensive security and environment management:

ENVIRONMENT SECURITY:

1. Secret Management:
   - Never commit secrets to Git
   - Use .env files for all secrets
   - .gitignore protects .env files
   - Provide .env.example template
   - Use environment variables in containers
   - Rotate secrets regularly

2. .env File Structure:
```
# Application Secrets
SECRET_KEY=generate-random-256-bit-key-here
FLASK_SECRET_KEY=another-random-key

# Database Credentials
DATABASE_URL=postgresql://user:strongpassword@localhost:5432/dbname
DB_PASSWORD=use-strong-password-here

# API Keys (Optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Service Tokens
ONLYOFFICE_SECRET=random-secret-here
REDIS_PASSWORD=redis-password-here

# Security Settings
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=3600
```

3. Environment Detection:
```python
# config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Fail fast if required secrets missing in production
    @classmethod
    def validate(cls):
        if os.getenv('FLASK_ENV') == 'production':
            required = ['SECRET_KEY', 'DATABASE_URL']
            missing = [key for key in required if not os.getenv(key)]
            if missing:
                raise ValueError(f"Missing required env vars: {missing}")
```

APPLICATION SECURITY:

1. Input Validation:
   - Validate all user inputs
   - Sanitize file uploads
   - Check file types and sizes
   - SQL injection prevention (use ORM)
   - XSS prevention (template escaping)
   - CSRF protection (Flask-WTF)

2. File Upload Security:
```python
UPLOAD_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.doc', '.docx'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
UPLOAD_FOLDER = '/var/www/app/uploads'  # Outside web root

def validate_upload(file):
    # Check extension
    # Check MIME type
    # Check file size
    # Scan for malware (optional)
    # Generate safe filename
```

3. Database Security:
   - Use parameterized queries (ORM handles this)
   - Least privilege database user
   - SSL/TLS for database connections
   - Regular backups
   - Connection encryption

4. API Security:
   - Rate limiting (Flask-Limiter)
   - API key authentication (if public API)
   - CORS configuration (Flask-CORS)
   - Request size limits
   - Timeout settings

5. Password Security (if user auth):
   - Bcrypt hashing
   - Salt for each password
   - Minimum password requirements
   - Password reset flow
   - Account lockout after failed attempts

DOCKER SECURITY:

1. Container Security:
   - Run as non-root user
   - Minimal base images
   - No secrets in Dockerfile
   - Read-only root filesystem where possible
   - Drop unnecessary capabilities
   - Security scanning (Trivy, Snyk)

2. Docker Compose Security:
```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true
    user: "1000:1000"  # Non-root
    read_only: true
    tmpfs:
      - /tmp
    environment:
      - SECRET_KEY=${SECRET_KEY}  # From .env file
```

LOGGING & MONITORING:

1. Security Logging:
   - Log authentication attempts
   - Log file access
   - Log API requests
   - Log errors and exceptions
   - No sensitive data in logs

2. Log Configuration:
```python
LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'default',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
}
```

PRODUCTION SECURITY CHECKLIST:
- [ ] Change all default passwords
- [ ] Generate new SECRET_KEY
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure firewall rules
- [ ] Disable debug mode
- [ ] Remove test/development users
- [ ] Set up automated backups
- [ ] Configure log rotation
- [ ] Enable security headers
- [ ] Set up monitoring/alerting
- [ ] Document security procedures
- [ ] Regular security updates
```

---

## 9. Testing & Verification Prompt

### 📝 Copy-Paste Prompt:

```
Create a comprehensive testing strategy with multiple test levels:

TEST STRUCTURE:

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── unit/                    # Unit tests
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utilities.py
├── integration/             # Integration tests
│   ├── test_database.py
│   ├── test_api.py
│   └── test_document_processing.py
├── e2e/                     # End-to-end tests
│   └── test_user_workflows.py
└── performance/             # Performance tests
    └── test_load.py
```

UNIT TESTS:

1. Service Layer Testing:
```python
# Test each service independently
def test_ocr_service():
    config = TestConfig()
    ocr_service = OCRService(config)
    
    # Test with mock file
    result = ocr_service.process_image(mock_image)
    
    assert result is not None
    assert 'text' in result
    assert len(result['text']) > 0
```

2. Model Testing:
```python
# Test database models
def test_document_model():
    doc = Document(filename='test.pdf', content='Test content')
    db.session.add(doc)
    db.session.commit()
    
    assert doc.id is not None
    assert doc.created_at is not None
```

INTEGRATION TESTS:

1. API Endpoint Testing:
```python
def test_upload_document(client):
    data = {'file': (io.BytesIO(b'test pdf'), 'test.pdf')}
    response = client.post('/api/documents/upload', data=data)
    
    assert response.status_code == 200
    assert 'document_id' in response.json
```

2. Database Integration:
```python
def test_database_connection():
    # Test connection
    result = db.session.execute('SELECT 1')
    assert result is not None
    
    # Test extensions
    result = db.session.execute("SELECT extname FROM pg_extension WHERE extname = 'vector'")
    assert result.fetchone() is not None
```

E2E TESTS:

1. Complete Workflow Testing:
```python
def test_document_to_chat_workflow(client):
    # Upload document
    upload_response = client.post('/api/documents/upload', ...)
    doc_id = upload_response.json['document_id']
    
    # Wait for processing
    time.sleep(2)
    
    # Query via chatbot
    chat_response = client.post('/api/chat', json={
        'message': 'What is in the document?'
    })
    
    assert 'response' in chat_response.json
    # Verify response mentions document content
```

HEALTH CHECK TESTS:

```python
def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = response.json
    assert data['status'] == 'healthy'
    assert 'database' in data['services']
    assert 'llm' in data['services']

def test_database_status(client):
    response = client.get('/api/database/status')
    assert response.status_code == 200
    
    data = response.json
    assert data['connected'] is True
    assert 'document_count' in data
```

CONFIGURATION TESTING:

```python
def test_config_validation():
    # Test missing required config
    with pytest.raises(ValueError):
        config = ProductionConfig()
        config.validate()
    
    # Test valid config
    os.environ['SECRET_KEY'] = 'test-key'
    os.environ['DATABASE_URL'] = 'postgresql://...'
    config = ProductionConfig()
    config.validate()  # Should not raise
```

PERFORMANCE TESTING:

1. Load Testing:
```python
# Use locust or pytest-benchmark
def test_api_performance(benchmark):
    result = benchmark(lambda: client.get('/api/health'))
    assert result.status_code == 200

def test_document_processing_time():
    start = time.time()
    result = ocr_service.process_document('large_doc.pdf')
    duration = time.time() - start
    
    assert duration < 30  # Should complete in 30 seconds
```

TEST FIXTURES:

```python
# conftest.py
@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_llm_service(monkeypatch):
    class MockLLM:
        def generate(self, prompt):
            return "Mock response"
    
    monkeypatch.setattr('app.services.llm_service.LLMService', MockLLM)
```

TEST DOCUMENTATION:

Create tests/README.md:
```markdown
# Running Tests

## All Tests
pytest

## Unit Tests Only
pytest tests/unit/

## Integration Tests
pytest tests/integration/

## With Coverage
pytest --cov=app --cov-report=html

## Specific Test
pytest tests/unit/test_services.py::test_ocr_service

## Verbose Output
pytest -v -s
```

CI/CD TESTING:

Create .github/workflows/test.yml:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest --cov=app
```
```

---

## 10. Documentation Standards Prompt

### 📝 Copy-Paste Prompt:

```
Create comprehensive documentation for developers, DevOps, and end users:

DOCUMENTATION STRUCTURE:

```
├── README.md                          # Project overview
├── QUICKSTART.md                      # 5-minute quick start
├── TECHNICAL_SPECIFICATIONS.md        # Architecture details
├── CHANGELOG.md                       # Version history
├── CONTRIBUTING.md                    # Contribution guidelines
├── LICENSE.md                         # License information
├── DEVOPS_CHECKLIST.md               # Deployment checklist
├── DEVELOPMENT_PROMPT_GUIDE.md       # This guide
│
├── docs/
│   ├── deployment/
│   │   ├── DEPLOYMENT_GUIDE.md       # Complete deployment guide
│   │   ├── DOCKER_DEPLOYMENT.md      # Docker-specific
│   │   ├── VM_DEPLOYMENT.md          # Virtual machine setup
│   │   └── DATABASE_SETUP.md         # Database configuration
│   │
│   ├── features/
│   │   ├── OCR_PROCESSING.md         # OCR feature docs
│   │   ├── AI_CHATBOT.md             # Chatbot integration
│   │   └── VECTOR_SEARCH.md          # Search functionality
│   │
│   ├── api/
│   │   ├── API_REFERENCE.md          # API documentation
│   │   ├── ENDPOINTS.md              # Endpoint list
│   │   └── AUTHENTICATION.md         # Auth flow
│   │
│   └── troubleshooting/
│       ├── COMMON_ISSUES.md          # Known problems
│       ├── FAQ.md                    # Frequently asked questions
│       └── DEBUG_GUIDE.md            # Debugging help
│
└── scripts/
    └── README.md                      # Scripts documentation
```

README.md TEMPLATE:

```markdown
# Project Name

One-line description of what the application does.

## Features

- Feature 1 with brief description
- Feature 2 with brief description
- Feature 3 with brief description

## Quick Start

### Prerequisites
- Requirement 1 (with version)
- Requirement 2 (with version)

### Installation
\`\`\`bash
git clone <repo-url>
cd project
cp .env.example .env
# Edit .env
python scripts/setup/setup_database.py
python server.py
\`\`\`

## Project Structure

Brief overview of directory structure with key directories explained.

## Configuration

Key configuration options explained with examples.

## Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Deployment Guide](docs/deployment/DEPLOYMENT_GUIDE.md)
- [API Reference](docs/api/API_REFERENCE.md)
- [Troubleshooting](docs/troubleshooting/COMMON_ISSUES.md)

## License

License information
```

CODE DOCUMENTATION:

1. Docstring Standards:
```python
def process_document(file_path: str, options: dict = None) -> dict:
    """
    Process a document through OCR pipeline.
    
    Args:
        file_path (str): Absolute path to the document file
        options (dict, optional): Processing options:
            - 'language' (str): OCR language (default: 'eng')
            - 'dpi' (int): Image DPI for PDF conversion (default: 300)
            - 'enhance' (bool): Apply image enhancement (default: True)
    
    Returns:
        dict: Processing results containing:
            - 'text' (str): Extracted text content
            - 'confidence' (float): OCR confidence score (0-1)
            - 'pages' (int): Number of pages processed
            - 'processing_time' (float): Time in seconds
    
    Raises:
        FileNotFoundError: If file_path doesn't exist
        ValueError: If file format is not supported
        OCRException: If OCR processing fails
    
    Example:
        >>> result = process_document('/path/to/doc.pdf')
        >>> print(result['text'])
        'Extracted text...'
    """
```

2. Inline Comments:
   - Explain WHY, not WHAT
   - Complex logic explained
   - Reference issue numbers for workarounds
   - TODO/FIXME/HACK markers

3. Type Hints:
```python
from typing import List, Dict, Optional, Union

def search_documents(
    query: str,
    filters: Optional[Dict[str, Union[str, int]]] = None,
    limit: int = 10
) -> List[Document]:
    """Search with type hints for better IDE support"""
    pass
```

API DOCUMENTATION:

Use OpenAPI/Swagger or document manually:

```markdown
# API Endpoints

## POST /api/documents/upload

Upload a document for processing.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - file: Document file (required)
  - language: OCR language (optional, default: 'eng')

**Response:**
\`\`\`json
{
  "document_id": "uuid-here",
  "filename": "document.pdf",
  "status": "processing",
  "estimated_time": 30
}
\`\`\`

**Status Codes:**
- 200: Success
- 400: Invalid file or parameters
- 413: File too large
- 500: Processing error

**Example:**
\`\`\`bash
curl -X POST http://localhost:5000/api/documents/upload \
  -F "file=@document.pdf" \
  -F "language=eng"
\`\`\`
```

CONFIGURATION DOCUMENTATION:

Document all .env variables:

```markdown
# Configuration Reference

## Required Variables

### SECRET_KEY
- Type: String
- Description: Flask secret key for session encryption
- Example: `SECRET_KEY=your-random-256-bit-key`
- Generate: `python -c "import secrets; print(secrets.token_hex(32))"`

### DATABASE_URL
- Type: Connection String
- Description: PostgreSQL database connection
- Format: `postgresql://user:password@host:port/database`
- Example: `DATABASE_URL=postgresql://app_user:password@localhost:5432/app_db`

## Optional Variables

### OLLAMA_BASE_URL
- Type: URL
- Description: Ollama API endpoint for local LLM
- Default: `http://localhost:11434`
- Required for: AI chatbot feature
```

CHANGELOG FORMAT:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.3.0] - 2025-11-02

### Added
- New feature X with description
- Support for Y integration
- Configuration option for Z

### Changed
- Improved performance of A
- Updated dependency B to version X.Y

### Fixed
- Bug where C would fail under condition D
- Memory leak in E component

### Deprecated
- Old method F (use G instead)

### Security
- Fixed vulnerability in H
```

DEVOPS DOCUMENTATION:

```markdown
# DevOps Checklist

## Pre-Deployment
- [ ] All environment variables configured
- [ ] Database initialized
- [ ] SSL certificates installed
- [ ] Firewall rules configured

## Deployment Steps
1. Clone repository
2. Configure .env file
3. Run deployment script
4. Verify health checks
5. Configure monitoring

## Post-Deployment
- [ ] Test all API endpoints
- [ ] Verify database connections
- [ ] Check log output
- [ ] Set up automated backups
- [ ] Configure alerts

## Monitoring
- Health endpoint: /api/health
- Metrics endpoint: /api/metrics
- Logs location: /var/log/app/

## Troubleshooting
See docs/troubleshooting/COMMON_ISSUES.md
```

VERSION CONTROL:

Document Git workflow:

```markdown
# Git Workflow

## Branches
- main: Production-ready code
- develop: Development branch
- feature/*: New features
- hotfix/*: Emergency fixes

## Commit Messages
Format: `type(scope): description`

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code refactoring
- test: Test additions
- chore: Maintenance

Example: `feat(chatbot): Add streaming response support`

## Versioning
Follow Semantic Versioning: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes
```
```

---

## 🎯 How to Use This Guide

### For New Projects:

1. **Start with Core Architecture** (Section 1)
   - Copy the prompt to AI assistant
   - Generate initial project structure
   - Review and customize

2. **Add Local Server Setup** (Section 2)
   - Define all local services needed
   - Configure connection strings
   - Test service detection

3. **Implement Configuration System** (Section 3)
   - Create .env.example with all variables
   - Build config.py with validation
   - Test configuration loading

4. **Set Up Database** (Section 4)
   - Create database setup script
   - Add migration support
   - Test database initialization

5. **Build Service Layer** (Section 5)
   - Create service classes
   - Implement service registry
   - Add health checks

6. **Add Deployment Options** (Section 6)
   - Create Dockerfile and docker-compose.yml
   - Write deployment scripts
   - Document deployment process

7. **Integrate AI/LLM** (Section 7) - If needed
   - Choose provider(s)
   - Implement LLM service
   - Add RAG if needed

8. **Secure the Application** (Section 8)
   - Set up environment management
   - Add input validation
   - Configure logging

9. **Write Tests** (Section 9)
   - Create test structure
   - Write unit tests
   - Add integration tests

10. **Document Everything** (Section 10)
    - Write README
    - Create deployment guide
    - Document API

### For Existing Projects:

1. **Identify Current Architecture**
   - Map existing structure
   - Document current configuration
   - List dependencies

2. **Choose Sections to Implement**
   - Start with Configuration (Section 3)
   - Add Local Server Support (Section 2)
   - Implement Service Layer (Section 5)

3. **Incremental Migration**
   - Move one feature at a time
   - Test after each change
   - Update documentation

### For AI Assistant Prompts:

Copy entire section prompts into:
- ChatGPT/Claude for code generation
- GitHub Copilot Chat for inline assistance
- VS Code Copilot for file generation

### For Team Development:

1. Share this guide with team
2. Use prompts as requirements documents
3. Create checklists from each section
4. Review code against prompt requirements

---

## 📚 Reference Implementation

**OCR Agent Pro v1.3.0** demonstrates all these patterns:
- Repository: https://github.com/onefsmedia/ocr-agent-pro
- All 10 sections fully implemented
- Production-ready example
- Comprehensive documentation

### Key Files to Reference:

- `app/__init__.py` - Application factory pattern
- `config.py` - Configuration management
- `app/services/` - Modular service architecture
- `server.py` - Production server launcher
- `docker-compose.yml` - Multi-service orchestration
- `.env.example` - Configuration template
- `docs/deployment/` - Deployment guides

---

## ✅ Quick Checklist

Use this checklist when starting a new project:

### Architecture
- [ ] Application factory pattern
- [ ] Modular service layer
- [ ] Separate routes/services/models
- [ ] Configuration over code
- [ ] Health check endpoints

### Local Infrastructure
- [ ] Database configurable (PostgreSQL)
- [ ] Cache optional (Redis)
- [ ] All services local-first
- [ ] Service detection on startup
- [ ] Graceful degradation

### Configuration
- [ ] .env.example provided
- [ ] All settings in .env
- [ ] Config validation
- [ ] Feature flags supported
- [ ] Multiple environment configs

### Deployment
- [ ] Docker Compose ready
- [ ] Native VM scripts
- [ ] Systemd service file
- [ ] Multiple deployment paths
- [ ] Rollback procedures

### Security
- [ ] Secrets in environment
- [ ] .gitignore protects secrets
- [ ] Input validation
- [ ] Secure defaults
- [ ] Security checklist

### Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Health check tests
- [ ] Performance tests
- [ ] CI/CD pipeline

### Documentation
- [ ] README.md complete
- [ ] QUICKSTART.md
- [ ] API documentation
- [ ] Deployment guide
- [ ] Troubleshooting docs

---

## 🆘 Support

**Questions about this guide?**
- Review OCR Agent Pro implementation
- Check example code in repository
- Create GitHub issue for clarifications

**Using this guide?**
- Star the repository
- Share with your team
- Contribute improvements

---

**Created:** November 2, 2025  
**Version:** 1.0  
**License:** MIT  
**Based on:** OCR Agent Pro v1.3.0 - Production Architecture
