# OCR Agent - Database Setup Guide

## Overview

The OCR Agent application supports both PostgreSQL (recommended) and SQLite (fallback) databases. This guide provides multiple setup options.

## Quick Start (SQLite Fallback)

✅ **Already Working!** The application automatically falls back to SQLite when PostgreSQL is not available.

- Database: SQLite (`ocr_agent.db`)
- Features: All panels work except pgvector similarity search
- Setup: None required - works out of the box

## PostgreSQL Setup (Recommended)

PostgreSQL provides better performance and pgvector support for advanced vector similarity search.

### Option 1: Automatic Setup Script

Run the automated setup script:

```powershell
cd "c:\OCR Agent"
python setup_database.py
```

This script will:
- Check if PostgreSQL is installed
- Create the `ocr_agent` database
- Create the `ocr_user` with proper permissions
- Test the connection

### Option 2: Manual PostgreSQL Installation

#### Step 1: Install PostgreSQL

**Method A: Official Installer**
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer and set a password for `postgres` user
3. Add PostgreSQL bin directory to PATH

**Method B: Using Chocolatey**
```powershell
# As Administrator
choco install postgresql
```

**Method C: Using Docker**
```powershell
docker run --name postgres-ocr -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgres:15
```

#### Step 2: Create Database and User

Connect to PostgreSQL as admin:
```sql
-- Connect as postgres user
psql -h localhost -U postgres

-- Create user and database
CREATE USER ocr_user WITH PASSWORD 'ocr_password';
CREATE DATABASE ocr_agent OWNER ocr_user;
GRANT ALL PRIVILEGES ON DATABASE ocr_agent TO ocr_user;

-- Connect to the new database
\c ocr_agent

-- Install pgvector extension (optional but recommended)
CREATE EXTENSION IF NOT EXISTS vector;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO ocr_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ocr_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ocr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ocr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ocr_user;
```

#### Step 3: Test Connection

```powershell
cd "c:\OCR Agent"
python -c "from app import create_app; app = create_app(); print('Database connection successful!')"
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=postgresql://ocr_user:ocr_password@localhost:5432/ocr_agent

# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# OCR Settings
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
USE_DEEPSEEK_OCR=true
DEEPSEEK_OCR_URL=http://localhost:8001

# OnlyOffice
ONLYOFFICE_URL=http://localhost:8000
ONLYOFFICE_SECRET=your-secret-here

# AI/LLM
OLLAMA_BASE_URL=http://localhost:11434
LM_STUDIO_BASE_URL=http://localhost:1234
DEFAULT_LLM_PROVIDER=ollama
```

### Database URL Formats

- **PostgreSQL**: `postgresql://user:password@host:port/database`
- **SQLite**: `sqlite:///path/to/database.db`
- **PostgreSQL with SSL**: `postgresql://user:password@host:port/database?sslmode=require`

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   ```
   FATAL: password authentication failed for user "ocr_user"
   ```
   - Solution: Run `setup_database.py` or manually create user
   - Check PostgreSQL is running: `pg_ctl status`

2. **Connection Refused**
   ```
   connection to server at "localhost" failed: Connection refused
   ```
   - Solution: Start PostgreSQL service
   - Windows: Services → PostgreSQL → Start
   - Command: `pg_ctl start`

3. **pgvector Extension Missing**
   ```
   extension "vector" is not available
   ```
   - Solution: Install pgvector extension
   - Most PostgreSQL distributions include it
   - Alternative: Use SQLite fallback (works without vectors)

### Force SQLite Mode

To temporarily use SQLite even when PostgreSQL is available:

```powershell
set DATABASE_URL=sqlite:///ocr_agent.db
python app.py
```

### Database Reset

To reset the database:

```powershell
# For SQLite
del ocr_agent.db

# For PostgreSQL
psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS ocr_agent; CREATE DATABASE ocr_agent OWNER ocr_user;"
```

## Performance Notes

### SQLite (Fallback)
- ✅ Perfect for development and testing
- ✅ No setup required
- ✅ All core features work
- ❌ No vector similarity search
- ❌ Limited concurrent users
- ❌ No advanced analytics

### PostgreSQL (Recommended)
- ✅ Production-ready performance
- ✅ pgvector support for AI features
- ✅ Concurrent users
- ✅ Advanced query capabilities
- ✅ Data integrity and ACID compliance
- ❌ Requires setup and maintenance

## Security Notes

**Default Development Credentials:**
- User: `ocr_user`
- Password: `ocr_password`
- Database: `ocr_agent`

⚠️ **Change these in production!**

For production:
1. Use strong passwords
2. Enable SSL connections
3. Configure firewall rules
4. Regular backups
5. Monitor access logs

## Next Steps

1. ✅ Database is now working with SQLite fallback
2. 🔄 Optionally setup PostgreSQL for enhanced features
3. 🔧 Configure OnlyOffice integration
4. 🤖 Setup local LLM (Ollama/LM Studio)
5. 📄 Test document upload and OCR processing

The application is ready to use with all enhanced Panel 3 (System Settings) and Panel 4 (Database Status) functionality!