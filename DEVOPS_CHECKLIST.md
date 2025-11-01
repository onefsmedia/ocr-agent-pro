# DevOps Deployment Checklist - OCR Agent Pro v1.3.0

**Repository:** https://github.com/onefsmedia/ocr-agent-pro

This document provides a complete checklist for DevOps engineers deploying OCR Agent Pro to production VMs.

---

## ✅ What's Included in Repository

### 🐳 Container Deployment (Recommended)

#### Docker/Podman Files
- ✅ **Dockerfile** - Production container image
- ✅ **Dockerfile.local** - Development container
- ✅ **Dockerfile.minimal** - Lightweight image
- ✅ **docker-compose.yml** - Full stack orchestration (App + PostgreSQL + Redis + OnlyOffice)
- ✅ **docker-compose.local.yml** - Local development stack
- ✅ **docker-compose.onlyoffice.yml** - OnlyOffice-specific setup

#### What's Included in Containers
- Python 3.11 runtime
- Tesseract OCR 4.0+ with English language
- PostgreSQL client libraries
- Gunicorn WSGI server
- All Python dependencies (Flask, SQLAlchemy, LangChain, etc.)
- Health check endpoints
- Non-root user security

### 📜 Deployment Scripts

#### PowerShell Scripts (Windows Server)
- ✅ **scripts/deployment/deploy-local.ps1** - Local Windows deployment
- ✅ **scripts/deployment/deploy-podman.ps1** - Podman deployment
- ✅ **scripts/deployment/deploy-onlyoffice.ps1** - OnlyOffice setup
- ✅ **scripts/deployment/install-postgresql.ps1** - PostgreSQL installation
- ✅ **scripts/deployment/start_server.ps1** - Server startup script

#### Python Setup Scripts
- ✅ **scripts/setup/setup_database.py** - Database initialization
- ✅ **scripts/setup/migrate_database.py** - Database migrations
- ✅ **scripts/setup/setup_onlyoffice.py** - OnlyOffice configuration
- ✅ **scripts/setup/install_french_ocr.py** - Additional OCR languages

### 📚 Documentation

- ✅ **docs/deployment/DEPLOYMENT_GUIDE.md** - Complete deployment guide (917 lines)
- ✅ **docs/deployment/DATABASE_SETUP.md** - PostgreSQL + pgvector setup
- ✅ **docs/deployment/PODMAN_DEPLOYMENT.md** - Podman-specific instructions
- ✅ **docs/deployment/WAITRESS_SETUP.md** - WSGI server setup
- ✅ **QUICKSTART.md** - Quick deployment (5 minutes)
- ✅ **README.md** - Project overview
- ✅ **TECHNICAL_SPECIFICATIONS.md** - Architecture details

### ⚙️ Configuration

- ✅ **.env.example** - Environment template with all variables
- ✅ **.env.production** - Production environment example
- ✅ **config.py** - Application configuration management
- ✅ **requirements.txt** - Python production dependencies
- ✅ **requirements-dev.txt** - Development dependencies

### 🚀 Server Entry Points

- ✅ **server.py** - Production server launcher (Waitress WSGI)
- ✅ **wsgi.py** - WSGI entry point for Gunicorn/uWSGI
- ✅ **app.py** - Application factory

---

## 🎯 Quick Deployment Options

### Option 1: Docker Compose (Fastest - 10 Minutes)

```bash
# Clone repository
git clone https://github.com/onefsmedia/ocr-agent-pro.git
cd ocr-agent-pro

# Configure environment
cp .env.example .env
nano .env  # Edit DATABASE_URL, SECRET_KEY, etc.

# Deploy full stack
docker-compose up -d

# Verify
docker-compose ps
curl http://localhost:5000/api/health
```

**Services Started:**
- OCR Agent App (port 5000)
- PostgreSQL 16 with pgvector (port 5432)
- Redis 7 (port 6379)
- OnlyOffice Document Server (port 8080)
- Celery worker (background tasks)

### Option 2: VM Installation (Ubuntu/Debian)

```bash
# Clone repository
git clone https://github.com/onefsmedia/ocr-agent-pro.git
cd ocr-agent-pro

# Install system dependencies
sudo apt update
sudo apt install -y python3.11 python3.11-venv postgresql-14 \
    tesseract-ocr redis-server poppler-utils

# Setup PostgreSQL with pgvector
sudo -u postgres psql
CREATE DATABASE ocr_agent;
CREATE USER ocr_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ocr_agent TO ocr_user;
\c ocr_agent
CREATE EXTENSION vector;
\q

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit configuration

# Initialize database
python scripts/setup/setup_database.py

# Start production server
python server.py
```

### Option 3: Systemd Service (Production Linux)

Create `/etc/systemd/system/ocr-agent.service`:

```ini
[Unit]
Description=OCR Agent Pro
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=ocr_user
Group=ocr_user
WorkingDirectory=/opt/ocr-agent-pro
Environment="PATH=/opt/ocr-agent-pro/.venv/bin"
ExecStart=/opt/ocr-agent-pro/.venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ocr-agent
sudo systemctl start ocr-agent
sudo systemctl status ocr-agent
```

---

## 📋 Pre-Deployment Requirements

### System Requirements

**Minimum (Development/Testing):**
- 4 CPU cores
- 8GB RAM
- 50GB storage
- Ubuntu 20.04+ / Windows Server 2019+ / CentOS 8+

**Recommended (Production):**
- 8+ CPU cores
- 32GB RAM
- 200GB SSD
- Load balancer support
- Backup storage

### External Dependencies

**Required:**
- PostgreSQL 12+ with pgvector extension
- Redis 6.0+ (for background tasks)
- Tesseract OCR 4.0+

**Optional:**
- OnlyOffice Document Server 7.4+ (document editing)
- Ollama / LM Studio (local LLM)
- OpenAI API key (cloud LLM)
- NGINX/Apache (reverse proxy)

### Network/Firewall

**Ports to Open:**
- 5000 - OCR Agent application
- 5432 - PostgreSQL (if external)
- 6379 - Redis (if external)
- 8080 - OnlyOffice Document Server
- 11434 - Ollama LLM (if used)

---

## 🔐 Security Checklist

- [ ] Change default SECRET_KEY in .env
- [ ] Use strong database passwords
- [ ] Enable PostgreSQL SSL/TLS
- [ ] Configure firewall rules
- [ ] Use HTTPS with valid SSL certificate
- [ ] Set up reverse proxy (NGINX)
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Restrict file upload sizes
- [ ] Regular security updates
- [ ] Database backups scheduled

---

## 🧪 Post-Deployment Testing

```bash
# Health check
curl http://localhost:5000/api/health

# Database connectivity
curl http://localhost:5000/api/database/status

# Upload test document
curl -X POST -F "file=@test.pdf" http://localhost:5000/api/documents/upload

# Vector search test
curl http://localhost:5000/api/search?q=test+query

# AI chatbot test
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what documents do you have?"}'
```

---

## 📊 Monitoring & Logs

### Application Logs
```bash
# Docker
docker logs ocr_agent_app -f

# Systemd
journalctl -u ocr-agent -f

# File logs
tail -f logs/app.log
```

### Health Monitoring
- **Health endpoint:** http://localhost:5000/api/health
- **Database status:** http://localhost:5000/api/database/status
- **Metrics:** Check logs/app.log for performance metrics

### Database Monitoring
```bash
# Check document count
python scripts/maintenance/check_documents.py

# PostgreSQL connections
psql -U ocr_user -d ocr_agent -c "SELECT count(*) FROM pg_stat_activity;"
```

---

## 🔧 Maintenance Scripts

Located in `scripts/maintenance/`:

- **check_documents.py** - Verify database documents
- **check-onlyoffice-status.py** - OnlyOffice health check
- **debug_chat.py** - Test chatbot functionality
- **verify_onlyoffice_8080.ps1** - Port verification

---

## 📦 What's NOT Included (External Requirements)

### ❌ Not in Repository:

1. **Production secrets** - You must provide:
   - Database passwords
   - SECRET_KEY
   - API keys (OpenAI, etc.)
   - OnlyOffice tokens

2. **SSL Certificates** - Must configure:
   - HTTPS certificates
   - Domain configuration
   - Reverse proxy setup

3. **LLM Models** - Must download separately:
   - Ollama models (llama3.3, etc.)
   - LM Studio models
   - Or configure OpenAI API

4. **OnlyOffice License** - For production use:
   - Community edition (included, limited connections)
   - Enterprise license (must purchase)

5. **Backup System** - Must implement:
   - Database backup strategy
   - Document storage backup
   - Configuration backup

---

## 🆘 Troubleshooting Resources

### Documentation
- `docs/troubleshooting/DOCKER_ISSUE_SUMMARY.md` - Docker problems
- `docs/troubleshooting/PROBLEM_RESOLVED.md` - Common issues
- `docs/troubleshooting/ONLYOFFICE_PORT_8000_MANUAL_GUIDE.md` - OnlyOffice issues

### Common Issues

**Database connection fails:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U ocr_user -d ocr_agent -h localhost
```

**Port already in use:**
```bash
# Find process using port 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows
```

**OCR not working:**
```bash
# Verify Tesseract installation
tesseract --version

# Test OCR
tesseract test.png output
```

---

## 📞 Support & Resources

- **Repository:** https://github.com/onefsmedia/ocr-agent-pro
- **Version:** 1.3.0 (Production Ready)
- **Issues:** Create GitHub issue for bugs
- **Documentation:** See docs/ directory
- **Changelog:** CHANGELOG.md

---

## ✅ Final Checklist

### Before Going Live:

- [ ] Clone repository from GitHub
- [ ] Install all system dependencies
- [ ] Configure .env with production values
- [ ] Initialize database with setup_database.py
- [ ] Test health endpoints
- [ ] Configure NGINX reverse proxy
- [ ] Enable HTTPS with SSL certificate
- [ ] Set up systemd service
- [ ] Configure firewall rules
- [ ] Test document upload and processing
- [ ] Test AI chatbot functionality
- [ ] Set up monitoring and alerting
- [ ] Configure automated backups
- [ ] Document your specific deployment details
- [ ] Train operations team

### Production Deployment Complete! 🎉

Access your application at: https://your-domain.com

---

**Last Updated:** November 2, 2025
**Version:** 1.3.0
**Status:** Production Ready ✅
