# OCR Agent - Project Organization Plan

**Date**: November 1, 2025  
**Purpose**: Consolidate and organize the project for production readiness and version control

---

## Current State Analysis

### Issues Identified:
1. **Multiple duplicate server launchers** (~20 files): `*_server.py`, `run*.py`
2. **Multiple test files** (~20 files): `test_*.py` with overlapping functionality
3. **Multiple OnlyOffice configuration scripts** (~15 files): `configure_onlyoffice*.py`, `*_onlyoffice*.py`
4. **Duplicate setup scripts**: `setup*.py`, `install*.py`
5. **PowerShell deployment duplicates**: `deploy*.ps1`, `configure*.ps1`
6. **Scattered documentation**: Multiple `.md` files with overlapping content
7. **No clear version history**: Old versions mixed with current production code

---

## Proposed Directory Structure

```
C:\OCR Agent\
│
├── app/                                    # Core application (KEEP AS IS)
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   ├── services/
│   ├── api/
│   └── templates/
│
├── static/                                 # Frontend assets (KEEP AS IS)
├── templates/                              # HTML templates (KEEP AS IS)
├── migrations/                             # Database migrations (KEEP AS IS)
├── instance/                               # Instance-specific data (KEEP AS IS)
├── storage/                                # File storage (KEEP AS IS)
├── uploads/                                # Upload directory (KEEP AS IS)
│
├── scripts/                                # NEW - Utility scripts
│   ├── deployment/
│   │   ├── deploy_docker.ps1
│   │   ├── deploy_podman.ps1
│   │   ├── deploy_local.ps1
│   │   └── README.md
│   ├── setup/
│   │   ├── setup_database.py
│   │   ├── setup_onlyoffice.py
│   │   ├── migrate_database.py
│   │   └── README.md
│   ├── configuration/
│   │   ├── configure_onlyoffice.py        # CANONICAL VERSION
│   │   ├── configure_large_files.py
│   │   └── README.md
│   └── maintenance/
│       ├── check_documents.py
│       ├── diagnostic.py
│       └── README.md
│
├── tests/                                  # NEW - All test files
│   ├── unit/
│   │   ├── test_ocr_service.py
│   │   ├── test_embedding_service.py
│   │   └── test_llm_service.py
│   ├── integration/
│   │   ├── test_api.py
│   │   ├── test_document_ingestion.py
│   │   └── test_onlyoffice_integration.py
│   ├── e2e/
│   │   ├── test_chatbot_comprehensive.py
│   │   └── test_application.py
│   └── README.md
│
├── docker/                                 # Docker configurations (KEEP AS IS)
│   ├── deepseek-ocr/
│   ├── docker-compose.yml
│   ├── docker-compose.local.yml
│   ├── Dockerfile
│   └── Dockerfile.minimal
│
├── docs/                                   # NEW - All documentation
│   ├── deployment/
│   │   ├── DEPLOYMENT_GUIDE.md
│   │   ├── PODMAN_DEPLOYMENT.md
│   │   ├── WAITRESS_SETUP.md
│   │   └── DATABASE_SETUP.md
│   ├── features/
│   │   ├── FEATURE_REVIEW.md
│   │   ├── CHATBOT_FIX_SUMMARY.md
│   │   └── ENHANCED_*.md
│   ├── technical/
│   │   ├── TECHNICAL_SPECIFICATIONS.md
│   │   └── API_DOCUMENTATION.md
│   └── troubleshooting/
│       ├── DOCKER_ISSUE_SUMMARY.md
│       └── PROBLEM_RESOLVED.md
│
├── _archive/                               # NEW - Old versions
│   ├── v1.0_initial/                      # Early prototypes
│   │   ├── servers/
│   │   ├── tests/
│   │   └── README.md
│   ├── v1.1_server_fixes/                 # Server stability work
│   │   ├── servers/
│   │   └── README.md
│   ├── v1.2_onlyoffice_integration/       # OnlyOffice integration attempts
│   │   ├── configuration/
│   │   ├── scripts/
│   │   └── README.md
│   └── deprecated/                         # Completely obsolete files
│       └── README.md
│
├── .github/                                # GitHub configurations (KEEP AS IS)
│   ├── copilot-instructions.md
│   └── workflows/                          # NEW - CI/CD pipelines
│       ├── tests.yml
│       ├── deploy.yml
│       └── code_quality.yml
│
├── logs/                                   # Application logs (KEEP AS IS)
├── .venv/                                  # Virtual environment (KEEP AS IS)
├── __pycache__/                            # Python cache (KEEP AS IS)
│
├── app.py                                  # ✅ CANONICAL - Application factory
├── config.py                               # ✅ CANONICAL - Configuration
├── requirements.txt                        # ✅ CANONICAL - Dependencies
├── requirements-dev.txt                    # NEW - Development dependencies
│
├── server.py                               # NEW - Production server launcher
├── wsgi.py                                 # NEW - WSGI entry point
│
├── .env.example                            # ✅ Environment template
├── .env.production                         # ✅ Production config template
├── .gitignore                              # NEW - Git ignore rules
│
├── README.md                               # ✅ CANONICAL - Main documentation
├── TECHNICAL_SPECIFICATIONS.md             # ✅ CANONICAL - Technical docs
├── LICENSE                                 # NEW - License file
└── CHANGELOG.md                            # NEW - Version history
```

---

## File Classification & Actions

### 1. Server Launchers (Choose ONE canonical, archive the rest)

**CANONICAL (Production):**
- ✅ **`server.py`** (NEW - to be created from `waitress_server.py`)
- ✅ **`wsgi.py`** (NEW - to be created for production WSGI)
- ✅ **`app.py`** (KEEP - Application factory)

**ARCHIVE to `_archive/v1.1_server_fixes/servers/`:**
- `waitress_server.py` → Most comprehensive, will become `server.py`
- `final_server.py` → Simple waitress implementation
- `stable_server.py` → Stable waitress version
- `stable_production_server.py` → Flask development server
- `production_server.py` → Waitress production
- `persistent_server.py` → Complex persistence logic
- `persistent_server_simple.py` → Simplified persistence
- `server_clean.py` → Clean implementation
- `professional_server.py` → Diagnostic server
- `clean_server.py` → Another clean variant
- `run_server.py` → FlaskAppManager implementation
- `start_server.py` → Generic launcher
- `dev_server.py` → Development server
- `simple_server.py` → Simple launcher
- `ultra_simple_server.py` → Ultra simple launcher
- `background_server.py` → Background thread server
- `minimal_server.py` → Minimal troubleshooting
- `isolated_server_launcher.py` → Subprocess isolation
- `flask_direct.py` → Direct Flask
- `quick_server.py` → Quick start
- `diagnostic.py` → Diagnostic server
- `run.py` → Simple run script
- `simple.py` → Another simple variant

**VERDICT:** Keep `waitress_server.py` logic, rename to `server.py`, archive all others.

---

### 2. Test Files (Organize by type)

**UNIT TESTS → `tests/unit/`:**
- `test_llm_integration.py` → LLM service tests
- `test_pdf_ocr.py` → OCR service tests
- `test_api.py` → API endpoint tests (could be integration)

**INTEGRATION TESTS → `tests/integration/`:**
- ✅ **`test_document_ingestion_final.py`** → CANONICAL ingestion test
- `test_document_ingestion.py` → Archive (older version)
- `test_onlyoffice_integration.py` → OnlyOffice integration
- `test_onlyoffice.py` → Archive (duplicate)
- `test_enhanced_ingestion.py` → Enhanced version
- `test_500mb_processing.py` → Large file processing
- `test_comprehensive_fixes.py` → Archive (troubleshooting)

**E2E TESTS → `tests/e2e/`:**
- ✅ **`test_chatbot_comprehensive.py`** → CANONICAL chatbot test
- ✅ **`test_application.py`** → CANONICAL application test
- `test_chat_comprehensive.py` → Archive (duplicate)
- `test_enhanced_chatbot.py` → Archive (older)
- `test_chatbot_direct.py` → Archive (troubleshooting)
- `test_chatbot_fix.py` → Archive (troubleshooting)
- `test_chatbot_manual.py` → Archive (manual testing)
- `test_chatbot_panel.py` → Archive (panel specific)
- `test_chatbot_ui.py` → Archive (UI specific)
- `test_chat_fix.py` → Archive (troubleshooting)
- `test_simple_chat.py` → Archive (simple version)
- `test_scrollable_sessions.py` → Archive (specific feature)

**VERDICT:** Keep comprehensive tests, move specific troubleshooting tests to archive.

---

### 3. OnlyOffice Configuration Scripts

**CANONICAL → `scripts/configuration/`:**
- ✅ **`configure_onlyoffice.py`** → Most complete version

**ARCHIVE to `_archive/v1.2_onlyoffice_integration/configuration/`:**
- `configure_onlyoffice_local.py` → Local configuration
- `configure_onlyoffice_detected.py` → Auto-detection
- `setup_onlyoffice.py` → Setup script
- `update_onlyoffice_port.py` → Port updates
- `force_update_onlyoffice.py` → Force update
- `find_onlyoffice_port.py` → Port detection
- `monitor_onlyoffice_8080.py` → Monitoring
- `scan_onlyoffice.py` → Port scanning
- `onlyoffice_port_helper.py` → Port helper
- `onlyoffice_admin_guide.py` → Admin guide script
- `onlyoffice_solution.py` → Integration test (move to tests)
- `check-onlyoffice-status.py` → Status check (move to scripts/maintenance)

**PowerShell Scripts → `scripts/configuration/`:**
- `configure_onlyoffice_port.ps1` → Archive (superseded)
- `configure_onlyoffice_port_8000.ps1` → Archive
- `configure_onlyoffice_port_8001.ps1` → Archive
- `configure_onlyoffice_port_admin.ps1` → Archive
- `configure_onlyoffice_persistent_8080.ps1` → Archive
- `configure_port_8000_simple.ps1` → Archive
- `verify_onlyoffice_8080.ps1` → Keep in scripts/maintenance

**VERDICT:** Keep one canonical Python script and one PowerShell verification script.

---

### 4. Setup & Installation Scripts

**CANONICAL → `scripts/setup/`:**
- ✅ **`setup_database.py`** → Database setup
- ✅ **`migrate_database.py`** → Database migration
- `install_french_ocr.py` → Move to scripts/setup (language specific)

**ARCHIVE to `_archive/deprecated/`:**
- `setup_waitress.py` → Integrated into main server
- `setup_cameroon_education.py` → Specific feature setup
- `setup_bilingual_cameroon_education.py` → Specific feature setup

**VERDICT:** Keep database and OCR language scripts, archive specific feature setups.

---

### 5. PowerShell Deployment Scripts

**CANONICAL → `scripts/deployment/`:**
- ✅ **`deploy-local.ps1`** → Local deployment
- ✅ **`deploy-podman.ps1`** → Podman deployment
- ✅ **`podman-deploy.ps1`** → Duplicate? (Check content)
- `deploy-onlyoffice.ps1` → OnlyOffice deployment
- `deploy-onlyoffice-podman.ps1` → OnlyOffice Podman

**ARCHIVE to `_archive/v1.0_initial/`:**
- `setup.ps1` → Old setup
- `database-options.ps1` → Database options
- `install-postgresql.ps1` → PostgreSQL install (keep if useful)
- `install-postgresql-native.ps1` → Native install
- `docker-complete-fix.ps1` → Docker troubleshooting
- `docker-targeted-fix.ps1` → Docker troubleshooting

**Batch Files → Archive to `_archive/deprecated/`:**
- `setup.bat`
- `start_server.bat`
- `start_production_server.bat`
- `start_waitress.bat`
- `start-docker.bat`
- `deploy-podman.bat`
- `fix-docker.bat`

**VERDICT:** Keep essential PowerShell deployment scripts, archive batch files and troubleshooting scripts.

---

### 6. Bootstrap Token & Admin Scripts

**ARCHIVE to `_archive/v1.2_onlyoffice_integration/admin/`:**
- `bootstrap_bypass_manual.py`
- `disable_bootstrap_token.ps1`
- `generate_bootstrap_token.ps1`
- `reset_onlyoffice_admin.ps1`
- `start_onlyoffice_admin.ps1`
- `access_onlyoffice_admin.ps1`
- `alternative_admin_access.ps1`
- `onlyoffice_setup_guide.ps1`
- `discover_password.py`

**VERDICT:** Archive all - admin panel not required for production.

---

### 7. Documentation Files

**CANONICAL → `docs/`:**
- ✅ **`README.md`** → Root (KEEP)
- ✅ **`TECHNICAL_SPECIFICATIONS.md`** → Root (KEEP)
- ✅ **`DEPLOYMENT_GUIDE.md`** → docs/deployment/
- ✅ **`DEPLOYMENT.md`** → Check if duplicate, merge or archive
- ✅ **`PODMAN_DEPLOYMENT.md`** → docs/deployment/
- ✅ **`WAITRESS_SETUP.md`** → docs/deployment/
- ✅ **`DATABASE_SETUP.md`** → docs/deployment/
- ✅ **`FEATURE_REVIEW.md`** → docs/features/
- ✅ **`ONLYOFFICE_PORT_8000_MANUAL_GUIDE.md`** → Archive (specific troubleshooting)

**ARCHIVE to `_archive/` or docs/historical/:**
- `CHATBOT_FIX_SUMMARY.md` → docs/features/ or archive
- `DOCUMENT_INGESTION_REPORT.md` → docs/features/ or archive
- `ENHANCED_CHAT_INTERFACE_COMPLETE.md` → docs/features/ or archive
- `ENHANCED_CONFIG_NAVIGATION_COMPLETE.md` → docs/features/ or archive
- `ENHANCED_PROMPT_LAYOUT_COMPLETE.md` → docs/features/ or archive
- `DEEPSEEK_INTEGRATION_COMPLETE.md` → docs/features/ or archive
- `BILINGUAL_EDUCATION_COMPLETE.md` → Archive (specific feature)
- `CAMEROON_EDUCATION_INTEGRATION.md` → Archive (specific feature)
- `500MB_PROCESSING_SUMMARY.md` → docs/features/ or archive
- `DOCKER_ISSUE_SUMMARY.md` → docs/troubleshooting/
- `PROBLEM_RESOLVED.md` → docs/troubleshooting/

**VERDICT:** Organize by purpose, move historical/troubleshooting docs to appropriate locations.

---

### 8. Configuration Files

**CANONICAL:**
- ✅ **`config.py`** → KEEP (main configuration)
- ✅ **`.env.example`** → KEEP (environment template)
- ✅ **`.env.production`** → KEEP (production template)
- ✅ **`requirements.txt`** → KEEP (dependencies)
- `config.py.backup` → DELETE (backup file)
- `waitress_config.json` → Archive (integrated into server.py)

**NEW FILES TO CREATE:**
- `requirements-dev.txt` → Development dependencies
- `.gitignore` → Git ignore rules
- `wsgi.py` → WSGI entry point
- `server.py` → Canonical production server
- `CHANGELOG.md` → Version history
- `LICENSE` → License file

---

### 9. Maintenance & Diagnostic Scripts

**KEEP → `scripts/maintenance/`:**
- ✅ **`check_documents.py`** → Document verification
- ✅ **`diagnostic.py`** → System diagnostics (rename to `system_diagnostic.py`)
- `debug_chat.py` → Keep for debugging
- `check-onlyoffice-status.py` → Keep for OnlyOffice monitoring

**ARCHIVE:**
- `configure_large_files.py` → Feature integrated, archive implementation details

---

### 10. Logs & Temporary Files

**DELETE:**
- `server_diagnostic.log` → Old log file
- `onlyoffice-documentserver.exe` → Binary file (should not be in repo)

---

## Version History & Changelog

### Version 1.0 (Initial Development)
- Basic Flask application structure
- Tesseract OCR integration
- Simple document upload
- SQLite database

### Version 1.1 (Server Stability)
- Multiple server launcher implementations
- Waitress WSGI server integration
- PostgreSQL database migration
- Connection reliability improvements

### Version 1.2 (OnlyOffice Integration)
- OnlyOffice Document Server integration
- Port configuration attempts (8000, 8001, 8080)
- Admin panel access troubleshooting
- Bootstrap token handling

### Version 1.3 (Current Production)
- ✅ Stable chatbot with proper error handling
- ✅ OnlyOffice running on port 8080
- ✅ Enhanced UI with scrollable sessions
- ✅ pgvector for semantic search
- ✅ Multi-LLM support (Ollama, LM Studio, OpenAI)
- ✅ Comprehensive documentation

---

## Implementation Steps

1. ✅ **Create directory structure**
2. ✅ **Create canonical `server.py`** from `waitress_server.py`
3. ✅ **Create `wsgi.py`** for production WSGI
4. ✅ **Organize tests** into unit/integration/e2e
5. ✅ **Move scripts** to appropriate directories
6. ✅ **Move documentation** to docs/
7. ✅ **Create archive directories** and move old files
8. ✅ **Create `.gitignore`**
9. ✅ **Create `CHANGELOG.md`**
10. ✅ **Create `requirements-dev.txt`**
11. ✅ **Update README.md** with new structure
12. ✅ **Update DEPLOYMENT_GUIDE.md** with new file locations
13. ✅ **Test that application still works** after reorganization
14. ✅ **Git commit with detailed message**

---

## Files to DELETE Permanently

- `config.py.backup` → Backup file
- `server_diagnostic.log` → Old log
- `onlyoffice-documentserver.exe` → Binary
- Any `__pycache__/` directories

---

## Post-Organization Checklist

- [ ] Application starts with `python server.py`
- [ ] Tests run with `pytest tests/`
- [ ] Database migrations work
- [ ] OnlyOffice integration functional
- [ ] Chatbot responds correctly
- [ ] Documentation updated
- [ ] `.gitignore` excludes unnecessary files
- [ ] README.md reflects new structure
- [ ] DEPLOYMENT_GUIDE.md updated
- [ ] All imports still work
- [ ] No broken file references

---

**End of Organization Plan**
