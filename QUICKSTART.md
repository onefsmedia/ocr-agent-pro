# Quick Start Guide - OCR Agent Pro v1.3.0

**Production-Ready | Organized | Well-Documented**

---

## 🚀 Getting Started (5 Minutes)

### 1. Clone and Setup

```bash
# Clone repository
git clone <your-repo-url>
cd ocr-agent

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Or (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Minimum required:
# - DATABASE_URL (PostgreSQL connection string)
# - SECRET_KEY (random string for Flask)
```

### 3. Initialize Database

```bash
# Run setup script
python scripts/setup/setup_database.py

# Or manually
flask db upgrade
```

### 4. Start Server

```bash
# Production server (Waitress WSGI)
python server.py

# Or development server
flask run
```

### 5. Access Application

Open browser: **http://localhost:5000**

---

## 📂 Project Navigation

### Need to...

**Deploy to production?**
→ `docs/deployment/DEPLOYMENT_GUIDE.md`

**Run tests?**
→ `pytest tests/` (see `tests/README.md`)

**Configure OnlyOffice?**
→ `python scripts/configuration/configure_onlyoffice.py`

**Check database?**
→ `python scripts/maintenance/check_documents.py`

**Troubleshoot issues?**
→ `docs/troubleshooting/`

**Understand architecture?**
→ `TECHNICAL_SPECIFICATIONS.md`

---

## 🗂️ Directory Structure

```
ocr-agent/
├── app/                    # ← Your code here
├── scripts/                # ← Utility scripts
│   ├── deployment/        #    Production deployment
│   ├── setup/             #    Initial setup
│   ├── configuration/     #    Runtime config
│   └── maintenance/       #    Diagnostics
├── tests/                  # ← Test suite
│   ├── unit/              #    Component tests
│   ├── integration/       #    Multi-component tests
│   └── e2e/               #    Full workflow tests
├── docs/                   # ← Documentation
│   ├── deployment/        #    Setup guides
│   ├── features/          #    Feature docs
│   └── troubleshooting/   #    Problem resolution
├── server.py              # ← Production launcher
├── wsgi.py                # ← WSGI entry point
└── requirements.txt       # ← Dependencies
```

---

## 🛠️ Common Tasks

### Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html

# Format code
black app/ tests/

# Lint code
flake8 app/ tests/
```

### Deployment

```bash
# Local production
python server.py

# Docker
docker-compose up -d

# Podman (Windows)
.\scripts\deployment\deploy-podman.ps1

# Linux (systemd service)
sudo systemctl start ocr-agent
```

### Maintenance

```bash
# Check document integrity
python scripts/maintenance/check_documents.py

# Verify OnlyOffice status
python scripts/maintenance/check-onlyoffice-status.py

# Debug chatbot
python scripts/maintenance/debug_chat.py
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview |
| `TECHNICAL_SPECIFICATIONS.md` | Architecture & APIs |
| `CHANGELOG.md` | Version history |
| `docs/deployment/DEPLOYMENT_GUIDE.md` | Complete deployment |
| `docs/features/FEATURE_REVIEW.md` | Feature overview |
| `scripts/README.md` | Utility scripts guide |
| `tests/README.md` | Testing guidelines |

---

## 🐛 Troubleshooting

### Server won't start
1. Check Python version: `python --version` (need 3.11+)
2. Check dependencies: `pip list`
3. Check database: `pg_isready` (PostgreSQL)
4. Check logs: `logs/app.log`

### Database errors
1. Verify PostgreSQL running
2. Check `.env` DATABASE_URL
3. Run migrations: `flask db upgrade`
4. Check setup: `python scripts/setup/setup_database.py`

### OnlyOffice not working
1. Check service: `python scripts/maintenance/check-onlyoffice-status.py`
2. Verify port 8080: `netstat -an | findstr 8080`
3. See: `docs/troubleshooting/`

### Import errors
1. Activate virtual environment
2. Reinstall: `pip install -r requirements.txt`
3. Check Python path: `echo $PYTHONPATH`

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Server starts: `python server.py`
- [ ] Homepage loads: http://localhost:5000
- [ ] Database connected: Check logs
- [ ] Tests pass: `pytest tests/`
- [ ] Documents can upload
- [ ] OCR processing works
- [ ] Chatbot responds

---

## 🎯 Next Steps

1. **Review Features**: `docs/features/FEATURE_REVIEW.md`
2. **Configure Settings**: Web UI → Settings Panel
3. **Upload Test Document**: Dashboard → Upload
4. **Try Chatbot**: Dashboard → Chat Panel
5. **Deploy to Production**: `docs/deployment/DEPLOYMENT_GUIDE.md`

---

## 📞 Getting Help

- **Documentation**: Check `docs/` directory
- **Troubleshooting**: `docs/troubleshooting/`
- **Technical Details**: `TECHNICAL_SPECIFICATIONS.md`
- **Version History**: `CHANGELOG.md`
- **GitHub Issues**: [Repository Issues]

---

## 📊 Version Info

**Version**: 1.3.0 (Production Ready)  
**Released**: November 1, 2025  
**Status**: ✅ Stable

**What's New in 1.3.0**:
- Clean project organization
- Production-ready server
- Comprehensive documentation
- Organized tests
- Easy deployment

See `CHANGELOG.md` for complete version history.

---

**🎉 You're ready to go! Start with `python server.py`**
