# Scripts Directory

This directory contains utility scripts organized by purpose.

## Directory Structure

### `/deployment/`
Production deployment scripts:
- `deploy-local.ps1` - Deploy to local machine
- `deploy-podman.ps1` - Deploy with Podman containers
- `install-postgresql.ps1` - PostgreSQL installation
- `start_server.ps1` - Server startup script

### `/setup/`
Initial setup and configuration:
- `setup_database.py` - Initialize PostgreSQL database with pgvector
- `migrate_database.py` - Run database migrations
- `setup_onlyoffice.py` - Configure OnlyOffice Document Server
- `install_french_ocr.py` - Install French language OCR support

### `/configuration/`
Runtime configuration scripts:
- `configure_onlyoffice.py` - OnlyOffice port and settings configuration
- `configure_large_files.py` - Large file processing setup

### `/maintenance/`
Maintenance and diagnostic tools:
- `check_documents.py` - Verify document integrity
- `check-onlyoffice-status.py` - OnlyOffice service status
- `debug_chat.py` - Chatbot debugging utility
- `verify_onlyoffice_8080.ps1` - Verify OnlyOffice port binding

## Usage

### Initial Setup
```bash
# 1. Setup database
python scripts/setup/setup_database.py

# 2. Configure OnlyOffice
python scripts/configuration/configure_onlyoffice.py

# 3. Install additional OCR languages (optional)
python scripts/setup/install_french_ocr.py
```

### Deployment
```powershell
# Local deployment
.\scripts\deployment\deploy-local.ps1

# Podman deployment
.\scripts\deployment\deploy-podman.ps1
```

### Maintenance
```bash
# Check system status
python scripts/maintenance/check_documents.py
python scripts/maintenance/check-onlyoffice-status.py
```

## Notes

- All scripts assume you are in the project root directory
- Ensure Python virtual environment is activated before running Python scripts
- PowerShell scripts require Windows PowerShell 5.1 or PowerShell Core 7+
