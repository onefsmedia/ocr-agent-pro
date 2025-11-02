# OCR Agent - Document Processing and AI Assistant

A comprehensive OCR application with Flask, PostgreSQL with pgvector, OnlyOffice integrations, and AI chatbot for intelligent document processing.

## Features

- **Multi-format OCR**: Process PDFs, images with Tesseract and DeepSeek OCR
- **Vector Search**: PostgreSQL with pgvector for semantic document search
- **OnlyOffice Integration**: Sync with OnlyOffice for document editing and collaboration
- **AI Chatbot**: RAG-powered assistant with local LLM support
- **6-Panel Dashboard**: Complete document management interface
- **Container Ready**: Docker/Podman deployment support

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+ with pgvector extension
- Tesseract OCR 4.0+
- OnlyOffice Document Server (optional)
- Docker/Podman (optional)

### Installation

1. Clone repository:
```bash
git clone <repository-url>
cd ocr-agent
```

2. Create virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

5. Initialize database:
```bash
python scripts/setup/setup_database.py
```

6. Start server:
```bash
python server.py
```

Access the application at http://localhost:5000

## Project Structure

```
ocr-agent/
├── app/                    # Core Flask application
│   ├── routes/            # API endpoints and views
│   ├── services/          # Business logic
│   ├── models.py          # Database models
│   └── __init__.py        # App factory
├── scripts/               # Utility scripts
│   ├── deployment/        # Deployment scripts
│   ├── setup/             # Initial setup scripts
│   ├── configuration/     # Configuration utilities
│   └── maintenance/       # Diagnostic tools
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── docs/                  # Documentation
│   ├── deployment/        # Deployment guides
│   ├── features/          # Feature documentation
│   └── troubleshooting/   # Problem resolution
├── docker/                # Container configurations
├── static/                # Frontend assets
├── templates/             # HTML templates
├── migrations/            # Database migrations
├── server.py              # Production server launcher
├── wsgi.py                # WSGI entry point
├── app.py                 # Application factory
├── config.py              # Configuration management
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── CHANGELOG.md           # Version history
└── README.md              # This file
```

## API Endpoints

- `POST /api/upload` - Upload documents for OCR processing
- `GET /api/documents` - List processed documents
- `POST /api/chat` - Chat with AI assistant
- `GET /api/search` - Vector similarity search

## Deployment

See [docs/deployment/DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md) for comprehensive deployment instructions.

### Quick Deployment Options

**Local Development:**
```bash
python server.py
```

**Docker:**
```bash
docker-compose up -d
```

**Podman:**
```powershell
.\scripts\deployment\deploy-podman.ps1
```

**Production (Linux):**
```bash
# With systemd service
sudo cp ocr-agent.service /etc/systemd/system/
sudo systemctl enable --now ocr-agent
```

## Documentation

- **[Technical Specifications](TECHNICAL_SPECIFICATIONS.md)** - Architecture and API reference
- **[Deployment Guide](docs/deployment/DEPLOYMENT_GUIDE.md)** - Complete deployment instructions
- **[DevOps Checklist](DEVOPS_CHECKLIST.md)** - Production deployment checklist
- **[Development Prompt Guide](DEVELOPMENT_PROMPT_GUIDE.md)** - Reusable prompts for similar projects
- **[Change Log](CHANGELOG.md)** - Version history
- **[Scripts Documentation](scripts/README.md)** - Utility scripts guide
- **[Tests Documentation](tests/README.md)** - Testing guidelines

## Development

### Running Tests
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Code Quality
```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

## Version

**Current Version:** 1.3.0 (Production Ready)

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Check [docs/troubleshooting/](docs/troubleshooting/)
- Review [TECHNICAL_SPECIFICATIONS.md](TECHNICAL_SPECIFICATIONS.md)
- Open an issue on GitHub