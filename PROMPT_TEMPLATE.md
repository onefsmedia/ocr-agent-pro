# Application Development Prompt Template

**Copy this template and customize for your specific application needs.**

---

## 🎯 Basic Application Prompt

```
Create a production-ready web application with the following requirements:

APPLICATION TYPE: [e.g., Document Processing, Data Analysis, Content Management]

CORE FEATURES:
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

TECHNOLOGY STACK:
- Backend: Flask 3.0+ with Python 3.11+
- Database: PostgreSQL 12+ with [extensions needed]
- Server: Waitress/Gunicorn WSGI
- Frontend: [HTML templates / React / Vue]
- Deployment: Docker + Native installation

ARCHITECTURE REQUIREMENTS:
✅ Local-first (runs completely on localhost)
✅ Configuration-driven (all settings in .env file)
✅ Modular services (independent service classes)
✅ Multiple deployment options (Docker, VM, Windows, Linux)
✅ Health check endpoints
✅ Comprehensive logging

PROJECT STRUCTURE:
app/
├── __init__.py          # Application factory
├── models.py            # Database models
├── routes/              # HTTP endpoints
├── services/            # Business logic
└── api/                 # API endpoints

scripts/
├── deployment/          # Deployment scripts
├── setup/               # Setup automation
└── maintenance/         # Diagnostic tools

ENVIRONMENT CONFIGURATION (.env):
[List all required environment variables]

DEPLOYMENT:
- Docker Compose with [list services]
- Native VM installation scripts
- Systemd service for production
```

---

## 🔧 Configuration-Driven Design Prompt

```
Implement configuration-driven architecture where ALL behavior is controlled via .env file:

REQUIRED .env VARIABLES:

# Application Settings
FLASK_ENV=production
SECRET_KEY=[generate random key]
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
DATABASE_POOL_SIZE=20

# Service URLs (all localhost)
[SERVICE_NAME]_URL=http://localhost:[PORT]

# Feature Flags (enable/disable features)
ENABLE_[FEATURE_1]=true
ENABLE_[FEATURE_2]=false

# Provider Selection (switch implementations)
[SERVICE]_PROVIDER=[option1|option2|option3]

# File Paths
UPLOAD_FOLDER=/path/to/uploads
STORAGE_PATH=/path/to/storage

# Performance Settings
MAX_WORKERS=4
TIMEOUT=120
CHUNK_SIZE=500

IMPLEMENTATION:
- All services read config in __init__
- No hardcoded values in code
- Feature flags control routes/services
- Provider factory pattern for swappable implementations
- Validation on startup with clear error messages
```

---

## 🗄️ Database Setup Prompt

```
Create PostgreSQL database setup with:

DATABASE: PostgreSQL [version]
EXTENSIONS:
- [extension1] for [purpose]
- [extension2] for [purpose]

MODELS:
1. [Model1] - [description]
   Fields: [list key fields]
   
2. [Model2] - [description]
   Fields: [list key fields]

SETUP REQUIREMENTS:
- Automated setup script: scripts/setup/setup_database.py
- Check database exists, create if needed
- Install required extensions
- Run migrations automatically
- Connection pooling configured
- Health check endpoint: /api/database/status

MIGRATIONS:
- Flask-Migrate for database migrations
- Upgrade/downgrade support
- Version control for migration files
```

---

## 🔌 Service Architecture Prompt

```
Create modular service layer with these services:

SERVICE 1: [Service Name]
Purpose: [What it does]
Dependencies: [External services/libraries needed]
Configuration:
- [SERVICE]_URL=http://localhost:[port]
- [SERVICE]_OPTION1=value
Methods:
- initialize() - Setup service
- health_check() - Return status
- [key_method]() - Main functionality

SERVICE 2: [Service Name]
Purpose: [What it does]
Dependencies: [External services/libraries needed]
Configuration:
- [Settings needed]
Methods:
- [List key methods]

PATTERN:
- Each service in app/services/[name]_service.py
- Inherit from BaseService
- Dependency injection via __init__
- Configuration from config object
- Graceful degradation if dependencies unavailable
- Comprehensive error handling
- Service registry for auto-loading
```

---

## 🐳 Deployment Prompt

```
Create multiple deployment options:

OPTION 1: Docker Compose
Services:
- app: Main application
- postgres: Database with [extensions]
- [service3]: [Description]
- [service4]: [Description]

Requirements:
- Health checks for all services
- Named volumes for persistence
- Environment variables from .env
- Network isolation
- Ports: [list ports]

OPTION 2: Native VM Installation
Support:
- Ubuntu 20.04/22.04
- CentOS 8+
- Windows Server 2019+

Scripts:
- scripts/deployment/install-dependencies.sh
- scripts/deployment/setup-environment.sh
- scripts/deployment/start-services.sh

OPTION 3: Production Service
- Systemd service file for Linux
- Windows Service support
- Auto-restart on failure
- Log rotation configured
```

---

## 🤖 AI/LLM Integration Prompt (Optional)

```
Integrate AI/LLM with multiple provider support:

LOCAL PROVIDERS (No Internet):
- Ollama (localhost:11434)
  Model: [model name]
- LM Studio (localhost:1234)
  Model: [model name]

CLOUD PROVIDERS (Optional):
- OpenAI API
- Anthropic Claude
- [Other provider]

CONFIGURATION (.env):
DEFAULT_LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=[model-name]
OPENAI_API_KEY=[optional]

FEATURES:
- Provider abstraction (common interface)
- Automatic fallback if provider unavailable
- Streaming responses
- Context management
- RAG support [if needed]

RAG SETUP (if applicable):
- Vector embeddings: [model name]
- Dimension: [number]
- Storage: PostgreSQL with pgvector
- Chunk size: [size]
- Top-K results: [number]
```

---

## 🔐 Security Prompt

```
Implement security best practices:

SECRET MANAGEMENT:
- All secrets in .env file
- .gitignore protects .env
- .env.example template provided
- No secrets in code or Docker images

VALIDATION:
- Input validation for all user inputs
- File upload restrictions:
  * Allowed extensions: [list]
  * Max size: [size]
  * MIME type checking
- SQL injection prevention (use ORM)
- XSS prevention (template escaping)

DOCKER SECURITY:
- Non-root user
- Minimal base image
- Read-only filesystem where possible
- Security scanning

API SECURITY:
- Rate limiting
- CORS configuration
- Request size limits
- Timeout settings

PRODUCTION CHECKLIST:
- [ ] Change SECRET_KEY
- [ ] Strong database passwords
- [ ] HTTPS enabled
- [ ] Firewall configured
- [ ] Debug mode disabled
- [ ] Logs sanitized
```

---

## 🧪 Testing Prompt

```
Create comprehensive test suite:

TEST STRUCTURE:
tests/
├── unit/              # Test individual functions/classes
├── integration/       # Test service interactions
└── e2e/              # Test complete workflows

REQUIRED TESTS:

1. Unit Tests:
   - Test each service method
   - Test model CRUD operations
   - Test utility functions
   - Mock external dependencies

2. Integration Tests:
   - Test API endpoints
   - Test database operations
   - Test service interactions
   - Test file processing

3. Health Check Tests:
   - Test /api/health endpoint
   - Test service status checks
   - Test database connectivity

4. E2E Tests:
   - Test complete user workflows
   - Test [key workflow 1]
   - Test [key workflow 2]

COMMANDS:
pytest                          # Run all tests
pytest tests/unit/              # Unit tests only
pytest --cov=app               # With coverage
pytest -v -s                   # Verbose output
```

---

## 📚 Documentation Prompt

```
Create comprehensive documentation:

REQUIRED DOCUMENTS:

1. README.md
   - Project overview
   - Features list
   - Quick start (5 minutes)
   - Project structure
   - Configuration guide
   - Links to other docs

2. QUICKSTART.md
   - Installation steps
   - Basic configuration
   - First run
   - Verification tests

3. docs/deployment/DEPLOYMENT_GUIDE.md
   - System requirements
   - Dependencies
   - Step-by-step deployment
   - All deployment options
   - Troubleshooting

4. TECHNICAL_SPECIFICATIONS.md
   - Architecture overview
   - Technology stack details
   - Data flow diagrams
   - API specifications

5. .env.example
   - All environment variables
   - Descriptions for each
   - Example values
   - Required vs optional marked

6. Code Documentation
   - Docstrings for all functions
   - Type hints
   - Inline comments for complex logic
   - API endpoint documentation
```

---

## 💡 Usage Instructions

### Step 1: Copy This Template
Save this file locally as `MY_PROJECT_PROMPT.md`

### Step 2: Customize
Fill in the brackets `[like this]` with your specific requirements:
- Replace `[Feature 1]` with actual feature names
- Replace `[Service Name]` with your service names
- Replace `[port]` with actual port numbers
- Add/remove sections as needed

### Step 3: Use with AI Assistant
Copy the customized sections and paste into:
- ChatGPT
- Claude
- GitHub Copilot Chat
- Any AI coding assistant

### Step 4: Generate Code
The AI will generate code following the patterns specified.

### Step 5: Iterate
Refine prompts based on output and re-generate as needed.

---

## 📋 Quick Checklist

Before starting development, ensure you've customized:

- [ ] Application type and core features
- [ ] Technology stack (database, services)
- [ ] All .env variables listed
- [ ] Service list and their purposes
- [ ] Database models defined
- [ ] Deployment options decided
- [ ] Security requirements specified
- [ ] Test strategy defined
- [ ] Documentation structure planned

---

## 🎨 Example: Simple API Application

Here's a filled-in example for reference:

```
Create a production-ready REST API application with the following requirements:

APPLICATION TYPE: User Management API

CORE FEATURES:
1. User registration and authentication
2. Profile management (CRUD operations)
3. Role-based access control
4. Activity logging

TECHNOLOGY STACK:
- Backend: Flask 3.0+ with Python 3.11+
- Database: PostgreSQL 14 with uuid-ossp extension
- Server: Gunicorn WSGI
- Frontend: REST API only (no UI)
- Deployment: Docker + Native installation

SERVICES:
1. AuthService - JWT token generation/validation
2. UserService - User CRUD operations
3. EmailService - Email notifications
4. LogService - Activity logging

.env CONFIGURATION:
DATABASE_URL=postgresql://user:pass@localhost:5432/userdb
SECRET_KEY=generate-random-key
JWT_EXPIRATION=3600
SMTP_SERVER=localhost
SMTP_PORT=1025
ENABLE_EMAIL=false

DEPLOYMENT:
- Docker Compose with app + postgres + mailhog
- Ubuntu 22.04 installation script
- Systemd service for production
```

---

## 🔗 References

For a complete working example implementing all these patterns:
**Repository:** https://github.com/onefsmedia/ocr-agent-pro

**Key Files to Study:**
- `DEVELOPMENT_PROMPT_GUIDE.md` - Detailed explanations
- `app/` - Reference implementation
- `docker-compose.yml` - Multi-service setup
- `.env.example` - Configuration template
- `scripts/` - Automation scripts

---

## 💾 Save This Template

**Recommended Location:**
```
C:\Dev\Templates\app-prompt-template.md
~/dev/templates/app-prompt-template.md
```

Keep it handy for starting new projects!

---

**Version:** 1.0  
**Last Updated:** November 2, 2025  
**Based on:** OCR Agent Pro v1.3.0 Architecture
