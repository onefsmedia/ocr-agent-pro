# OCR Agent - Technical Specifications

**Version**: 1.3.0  
**Last Updated**: November 1, 2025  
**Status**: Production Ready

---

## 1. Architecture Overview

### System Architecture
```
┌─────────────────────────────────────────────────────┐
│                    Client Browser                   │
│              (HTML/CSS/JavaScript)                  │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/HTTPS
┌──────────────────────▼──────────────────────────────┐
│              Nginx Reverse Proxy                    │
│        (SSL/TLS, Load Balancing, Caching)          │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│          Flask Application Server                   │
│         (Gunicorn with Multiple Workers)           │
│  ┌─────────────────────────────────────────────┐   │
│  │ Routes & Controllers                        │   │
│  │ ┌─────────────────────────────────────────┐ │   │
│  │ │ Document Ingestion Panel                │ │   │
│  │ │ Table View Panel                        │ │   │
│  │ │ Settings Panel                          │ │   │
│  │ │ Database Status Panel                   │ │   │
│  │ │ Chatbot Panel                           │ │   │
│  │ │ Prompt Configuration Panel              │ │   │
│  │ └─────────────────────────────────────────┘ │   │
│  │ Middleware (Auth, Error Handling, Logging) │   │
│  └─────────────────────────────────────────────┘   │
└──────────┬──────────────────────┬──────────────────┘
           │                      │
           │                      │
    ┌──────▼─────┐      ┌────────▼──────┐
    │ PostgreSQL │      │   Redis       │
    │ Database   │      │   Cache/Queue │
    │ (pgvector) │      │               │
    └────────────┘      └───────────────┘
           │                      │
    ┌──────▼─────────────────────▼──────┐
    │    Celery Task Workers             │
    │  (Background Processing)           │
    │  - OCR Processing                  │
    │  - Document Indexing               │
    │  - Embedding Generation            │
    └────────────────────────────────────┘
           │
    ┌──────▼────────────────────────────┐
    │   External Services               │
    │  - DeepSeek OCR                   │
    │  - OnlyOffice Document Server     │
    │  - Ollama/LM Studio/OpenAI        │
    │  - Sentence Transformers          │
    └──────────────────────────────────┘
```

### Component Interaction Flow
```
User Upload
    │
    ├─► Validation
    │
    ├─► Storage
    │
    ├─► Queue (Celery)
    │
    ├─► OCR Processing
    │   ├─► Tesseract
    │   └─► DeepSeek OCR (optional)
    │
    ├─► Text Extraction
    │
    ├─► Chunking
    │
    ├─► Embedding Generation
    │   └─► pgvector Storage
    │
    ├─► Database Storage
    │
    └─► Ready for Search/Chat
```

---

## 2. Module Specifications

### 2.1 Document Ingestion Module

**Purpose**: Handle document upload, validation, and initial processing

**Key Files**:
- `app/routes/documents.py` - API endpoints
- `app/services/document_service.py` - Business logic
- `app/models/document.py` - Data models

**Capabilities**:
- Supported formats: PDF, DOC, DOCX, TXT, PNG, JPG, TIFF
- Max file size: 500MB
- Batch upload support: up to 10 files simultaneously
- Metadata extraction: author, creation date, pages, language

**API Endpoints**:
```
POST   /api/documents/upload          - Upload document
GET    /api/documents                 - List documents
GET    /api/documents/<id>            - Get document details
DELETE /api/documents/<id>            - Delete document
POST   /api/documents/<id>/reprocess  - Reprocess document
```

**Processing Pipeline**:
1. File validation (size, format, virus scan)
2. Storage to disk
3. Metadata extraction
4. Queue for OCR processing
5. Background processing via Celery

### 2.2 OCR Processing Module

**Purpose**: Extract text from documents using multiple OCR engines

**Key Files**:
- `app/services/ocr_service.py` - OCR orchestration
- `app/services/tesseract_ocr.py` - Tesseract integration
- `app/services/deepseek_ocr.py` - DeepSeek integration

**Supported Engines**:
1. **Tesseract 4.0+**
   - Open-source, free
   - Languages: 100+
   - Accuracy: 85-95% for clean documents
   
2. **DeepSeek OCR** (Optional)
   - AI-powered, higher accuracy
   - Languages: 30+
   - Accuracy: 92-98% for complex documents

**Language Support**:
- English, French, Spanish, German, Italian
- Arabic, Chinese, Japanese, Korean
- Russian, Portuguese, Dutch, Turkish
- Cameroon French (Français du Cameroun)

**Processing Parameters**:
```python
OCR_CONFIG = {
    'language': 'fra+eng',          # Multi-language
    'quality': 'high',               # low/medium/high
    'dpi': 300,                      # Resolution
    'pages': None,                   # None = all, or [1,2,3]
    'timeout': 300,                  # Seconds
    'retry_count': 3,                # Retries on failure
    'cache_results': True            # Cache intermediate results
}
```

### 2.3 Vector Embedding & Search Module

**Purpose**: Generate embeddings and enable semantic search

**Key Files**:
- `app/services/embedding_service.py` - Embedding generation
- `app/services/search_service.py` - Search functionality
- `app/models/document_chunk.py` - Chunk data model

**Technology Stack**:
- Model: `all-MiniLM-L6-v2` (Sentence Transformers)
- Dimensions: 384D vectors
- Database: PostgreSQL pgvector
- Search Method: Cosine similarity

**Chunking Strategy**:
- Chunk size: 500 tokens (configurable)
- Overlap: 50 tokens (configurable)
- Strategy: Smart chunking based on sentence boundaries

**Performance Metrics**:
- Embedding generation: ~50 documents/minute (CPU)
- Search latency: <100ms per query
- Index size: ~1MB per 1M vectors

### 2.4 AI Chatbot Module

**Purpose**: Provide conversational interface with document context

**Key Files**:
- `app/routes/chat.py` - Chat API
- `app/services/chat_service.py` - Chat logic
- `app/models/chat_session.py` - Session management

**Supported LLM Providers**:

1. **Ollama** (Local, Recommended)
   - Model: `llama3.3:latest`
   - RAM required: 8GB minimum
   - Speed: Low latency (~1-2s per response)
   - Cost: Free

2. **LM Studio** (Local)
   - Supports various models
   - GUI-based setup
   - Similar performance to Ollama

3. **OpenAI** (Cloud)
   - Model: GPT-4 Turbo / GPT-3.5 Turbo
   - Speed: Fast (< 500ms)
   - Cost: $0.01-0.03 per 1K tokens

**Chat Features**:
- Multi-turn conversations
- Document context awareness (RAG)
- Session persistence
- User history tracking
- Response streaming
- Follow-up question suggestions

**API Endpoints**:
```
POST   /api/chat/sessions            - Create session
GET    /api/chat/sessions            - List sessions
GET    /api/chat/sessions/<id>       - Get session
POST   /api/chat/send                - Send message
GET    /api/chat/history/<session_id>- Get chat history
DELETE /api/chat/sessions/<id>       - Delete session
```

### 2.5 OnlyOffice Integration Module

**Purpose**: Document editing and format conversion

**Key Files**:
- `app/services/onlyoffice_service.py` - OnlyOffice integration
- `app/routes/onlyoffice.py` - OnlyOffice endpoints

**Features**:
- Document format conversion (PDF, DOCX, XLSX, etc.)
- Online document editing
- Collaborative editing support
- Version tracking
- Export functionality

**Configuration**:
```
ONLYOFFICE_URL: http://localhost:8080
ONLYOFFICE_SECRET: your-secret-key
DOCUMENT_FORMATS: ['docx', 'xlsx', 'pptx', 'pdf', 'txt']
CONVERSION_TIMEOUT: 60 seconds
```

### 2.6 Settings Management Module

**Purpose**: Manage application configuration

**Key Files**:
- `app/routes/settings.py` - Settings API
- `app/services/settings_service.py` - Settings logic
- `app/models/system_settings.py` - Settings model

**Configurable Settings**:
- System prompt for AI
- OCR method selection
- LLM provider selection
- Embedding model
- Chunking parameters
- OnlyOffice connection
- Database connection
- Redis connection
- API rate limits

---

## 3. Database Schema

### Core Tables

#### documents
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    file_type VARCHAR(50),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    status VARCHAR(50),  -- pending, processing, completed, failed
    ocr_text TEXT,
    metadata JSONB,
    user_id INTEGER REFERENCES users(id)
);
```

#### document_chunks
```sql
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    chunk_number INTEGER,
    content TEXT NOT NULL,
    tokens INTEGER,
    embedding vector(384),  -- pgvector extension
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ON document_chunks USING IVFFLAT (embedding vector_cosine_ops);
```

#### chat_sessions
```sql
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    context JSONB
);
```

#### chat_messages
```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20),  -- user, assistant
    content TEXT NOT NULL,
    tokens INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);
```

#### system_settings
```sql
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    setting_type VARCHAR(50),
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. API Specification

### Authentication
```
Header: Authorization: Bearer {token}
Or: Cookie: session_id={session_id}
```

### Error Response Format
```json
{
    "success": false,
    "error": "Error description",
    "code": "ERROR_CODE",
    "timestamp": "2025-11-01T12:00:00Z"
}
```

### Success Response Format
```json
{
    "success": true,
    "data": {...},
    "timestamp": "2025-11-01T12:00:00Z"
}
```

### Rate Limiting
- Default: 100 requests per hour per IP
- Authenticated: 1000 requests per hour per user
- Upload: 10 files per hour

---

## 5. Performance Specifications

### Response Time Targets
- Home page load: < 500ms
- Document upload: < 2s
- Search query: < 500ms
- Chat response: < 5s (with streaming)
- Settings update: < 1s

### Scalability Metrics
- **Concurrent users**: 1000+ (with proper infrastructure)
- **Documents**: Unlimited (storage dependent)
- **Queries per second**: 100+ (read), 50+ (write)
- **Throughput**: 10,000 documents/day

### Resource Requirements

**Per Instance**:
- CPU: 4 cores minimum
- RAM: 8GB minimum
- Storage: 50GB minimum
- Network: 1Gbps

**For 10,000 concurrent users**:
- CPU: 64+ cores
- RAM: 128GB+
- Storage: 500GB+ SSD
- Database: Dedicated PostgreSQL cluster

---

## 6. Security Specifications

### Authentication & Authorization
- JWT tokens with 24-hour expiration
- Refresh token rotation
- Role-based access control (RBAC)
- Multi-factor authentication (optional)

### Data Protection
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.2+)
- Password hashing (bcrypt with salt)
- Sensitive data masking in logs

### Compliance
- GDPR compliant data handling
- CCPA compliance
- HIPAA considerations for health data
- Data retention policies

---

## 7. Development Standards

### Code Structure
```
ocr_agent/
├── app/
│   ├── __init__.py              # App initialization
│   ├── models/                  # Database models
│   ├── routes/                  # API endpoints
│   ├── services/                # Business logic
│   ├── utils/                   # Utility functions
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, images
├── tests/                       # Unit & integration tests
├── migrations/                  # Database migrations
├── config.py                    # Configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── wsgi.py                      # WSGI entry point
```

### Code Quality Standards
- Python 3.11+
- PEP 8 compliance (flake8)
- Type hints for functions
- Docstrings for all public methods
- Unit test coverage: > 80%
- Integration test coverage: > 60%

### Git Workflow
```
main branch (production)
    ↑
    ├─ release/* (release candidates)
    │
    ├─ develop (staging)
    │
    └─ feature/* (feature branches)
```

---

## 8. Deployment Checklist

### Pre-Deployment
- [ ] All tests passing (unit, integration, e2e)
- [ ] Code review completed
- [ ] Security scan passed
- [ ] Performance benchmarks acceptable
- [ ] Documentation updated
- [ ] Database migrations tested
- [ ] Dependencies updated and compatible

### Deployment
- [ ] Environment variables configured
- [ ] Database backup created
- [ ] Services restarted in correct order
- [ ] Health checks passing
- [ ] Smoke tests successful
- [ ] Monitoring alerts configured

### Post-Deployment
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Verify all features working
- [ ] Test user access
- [ ] Update deployment documentation
- [ ] Notify stakeholders

---

## 9. Monitoring & Alerting

### Key Metrics
- Application response time (average, p95, p99)
- Error rate (5xx, 4xx)
- Database query time
- Cache hit rate
- Memory usage
- Disk usage
- Network I/O
- Active concurrent users

### Alert Thresholds
- Response time > 2s: Warning
- Error rate > 1%: Alert
- Memory > 85%: Warning
- Disk > 90%: Alert
- CPU > 80%: Warning

---

## 10. Disaster Recovery

### Recovery Time Objective (RTO): 4 hours
### Recovery Point Objective (RPO): 1 hour

### Backup Strategy
- Daily incremental backups
- Weekly full backups
- Monthly archival backups
- Geo-distributed backups (optional)

### Failover Procedure
1. Detect failure (automated)
2. Stop failed instance
3. Start backup instance
4. Update DNS/load balancer
5. Restore data from backup
6. Verify functionality

---

## 11. Support & Maintenance

### SLA Commitments
- **Critical bugs**: Fix within 4 hours
- **High priority**: Fix within 24 hours
- **Normal priority**: Fix within 1 week
- **Low priority**: Fix within 1 month

### Maintenance Windows
- Tuesday 2:00 AM - 4:00 AM UTC
- Sunday 3:00 AM - 5:00 AM UTC
- Planned maintenance: 1 week notice

---

## 12. Future Enhancements

### Version 1.4 (Q1 2025)
- [ ] Advanced search filters
- [ ] Document annotation tools
- [ ] Collaborative features
- [ ] Mobile app

### Version 1.5 (Q2 2025)
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] API marketplace integration
- [ ] Custom model training

### Version 2.0 (Q4 2025)
- [ ] Multi-tenant support
- [ ] Enterprise authentication
- [ ] Advanced reporting
- [ ] AI-powered insights

---

**End of Technical Specifications Document**
