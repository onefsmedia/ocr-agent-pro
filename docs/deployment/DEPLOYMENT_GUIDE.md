# OCR Agent - Complete Deployment Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Dependencies](#dependencies)
3. [Environment Configuration](#environment-configuration)
4. [Installation Steps](#installation-steps)
5. [Database Setup](#database-setup)
6. [Service Configuration](#service-configuration)
7. [Deployment Options](#deployment-options)
8. [Testing & Verification](#testing--verification)
9. [Troubleshooting](#troubleshooting)
10. [Security Considerations](#security-considerations)

---

## System Requirements

### Minimum Hardware (Development/Small Deployments)
- **CPU**: 4 cores minimum
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB minimum (for documents and models)
- **Network**: 1Gbps minimum

### Production Hardware (Enterprise)
- **CPU**: 8+ cores (16+ recommended)
- **RAM**: 32GB+ recommended
- **Storage**: 200GB+ SSD for optimal performance
- **Network**: 10Gbps preferred

### Operating Systems Supported
- **Linux**: Ubuntu 20.04 LTS, 22.04 LTS, CentOS 8+
- **Windows**: Windows Server 2019, 2022
- **macOS**: 12.0+
- **Cloud Platforms**: AWS, Azure, DigitalOcean, Linode, Hetzner

---

## Dependencies

### Core Technology Stack

#### Backend Framework
- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM
- **Flask-Migrate 4.0.5** - Database migrations
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing

#### Database
- **PostgreSQL 12+** (with pgvector extension for vector search)
- **Redis 6.0+** (for caching and task queue)
- **psycopg2-binary 2.9.9** - PostgreSQL adapter

#### OCR & Document Processing
- **Tesseract 4.0+** - Open-source OCR
- **pdf2image 1.16.3** - PDF to image conversion
- **PyPDF2 3.0.1** - PDF manipulation
- **Pillow 10.1.0** - Image processing
- **pytesseract 0.3.10** - Tesseract Python wrapper

#### DeepSeek OCR Integration (Optional)
- **DeepSeek-OCR** - Advanced OCR engine
- **vLLM** - Vector LLM inference server

#### AI & Machine Learning
- **sentence-transformers 2.2.2** - Text embeddings
- **langchain 0.1.0** - LLM orchestration
- **openai 1.3.7** - OpenAI API client
- **numpy 1.24.3** - Numerical computing
- **pgvector 0.2.4** - PostgreSQL vector extension

#### Async & Task Processing
- **celery 5.3.4** - Distributed task queue
- **redis 5.0.1** - Redis Python client

#### Security
- **cryptography 41.0.7** - Cryptographic functions
- **PyJWT 2.8.0** - JWT token handling

#### Server & API
- **gunicorn 21.2.0** - WSGI HTTP server
- **Werkzeug 3.0.1** - WSGI utilities
- **requests 2.31.0** - HTTP library
- **httpx 0.25.2** - Async HTTP client

#### Monitoring & Logging
- **python-json-logger 2.0.7** - JSON logging

#### OnlyOffice Integration
- **OnlyOffice Document Server 7.4+** - Document editing and conversion

---

## Environment Configuration

### Create `.env` File

Create a `.env` file in the project root directory:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=your-very-secure-secret-key-here-change-this

# Database Configuration
DATABASE_URL=postgresql://ocr_user:secure_password@localhost:5432/ocr_agent_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
SERVER_WORKERS=4
SERVER_WORKER_CLASS=sync
SERVER_TIMEOUT=120

# Upload & Storage
UPLOAD_FOLDER=/var/www/ocr_agent/uploads
MAX_CONTENT_LENGTH=524288000  # 500MB in bytes
STORAGE_PATH=/var/www/ocr_agent/storage

# OCR Configuration
TESSERACT_PATH=/usr/bin/tesseract
USE_DEEPSEEK_OCR=true
DEEPSEEK_OCR_URL=http://localhost:8001
DEEPSEEK_OCR_PATH=/opt/deepseek-ocr

# OnlyOffice Configuration
ONLYOFFICE_URL=http://localhost:8080
ONLYOFFICE_SECRET=your-onlyoffice-secret-key
ONLYOFFICE_TOKEN=your-onlyoffice-token
ONLYOFFICE_STORAGE_URL=http://localhost:5000/storage

# LLM Configuration
DEFAULT_LLM_PROVIDER=ollama  # Options: ollama, lm_studio, openai
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.3:latest
LM_STUDIO_BASE_URL=http://localhost:1234
OPENAI_API_KEY=your-openai-key-here

# Vector Embedding
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=redis-secure-password

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/ocr_agent/app.log

# Security
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
SESSION_TIMEOUT=3600

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Feature Flags
ENABLE_CHAT=true
ENABLE_OCR=true
ENABLE_DEEPSEEK_OCR=true
ENABLE_ONLYOFFICE=true
```

### Example `.env` Files for Different Environments

#### Development (.env.development)
```bash
FLASK_ENV=development
DEBUG=true
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/ocr_agent_dev
LOG_LEVEL=DEBUG
SERVER_WORKERS=1
```

#### Production (.env.production)
```bash
FLASK_ENV=production
DEBUG=false
DATABASE_URL=postgresql://prod_user:very_secure_password@db-server.internal:5432/ocr_agent_prod
LOG_LEVEL=WARNING
SERVER_WORKERS=8
```

#### Staging (.env.staging)
```bash
FLASK_ENV=staging
DEBUG=false
DATABASE_URL=postgresql://staging_user:staging_password@staging-db:5432/ocr_agent_staging
LOG_LEVEL=INFO
SERVER_WORKERS=4
```

---

## Installation Steps

### 1. System-Level Dependencies (Ubuntu/Debian)

```bash
# Update package manager
sudo apt-get update && sudo apt-get upgrade -y

# Install Python and development tools
sudo apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    git

# Install OCR dependencies
sudo apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-all \
    libtesseract-dev

# Install image processing dependencies
sudo apt-get install -y \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    libopenjp2-7-dev \
    libtiff-dev \
    libwebp-dev

# Install database client
sudo apt-get install -y postgresql-client

# Install additional utilities
sudo apt-get install -y \
    build-essential \
    curl \
    wget \
    nano \
    vim
```

### 2. Create Application Directory

```bash
# Create application directory
sudo mkdir -p /var/www/ocr_agent
sudo chown $USER:$USER /var/www/ocr_agent
cd /var/www/ocr_agent

# Create necessary subdirectories
mkdir -p uploads storage logs migrations
chmod 755 uploads storage logs
```

### 3. Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/ocr-agent.git .
# or
git clone git@github.com:yourusername/ocr-agent.git .
```

### 4. Set Up Python Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel
```

### 5. Install Python Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Install gunicorn for production
pip install gunicorn

# Optional: Install supervisor for process management
sudo apt-get install -y supervisor
```

### 6. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit with your configuration
nano .env

# Set proper permissions
chmod 600 .env
```

---

## Database Setup

### 1. PostgreSQL Installation and Configuration

#### Ubuntu/Debian:
```bash
# Install PostgreSQL 14
sudo apt-get install -y postgresql postgresql-contrib postgis

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Connect to PostgreSQL
sudo -u postgres psql
```

#### Create Database and User:
```sql
-- Create database
CREATE DATABASE ocr_agent_db;

-- Create user
CREATE USER ocr_user WITH ENCRYPTED PASSWORD 'secure_password_here';

-- Grant privileges
ALTER ROLE ocr_user SET client_encoding TO 'utf8';
ALTER ROLE ocr_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ocr_user SET default_transaction_deferrable TO on;
ALTER ROLE ocr_user SET default_transaction_level TO 'read committed';
ALTER ROLE ocr_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ocr_agent_db TO ocr_user;

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
GRANT USAGE ON SCHEMA public TO ocr_user;

-- Exit psql
\q
```

### 2. Initialize Flask Database

```bash
# Activate virtual environment
source venv/bin/activate

# Run database initialization
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Or use the init_db command
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 3. Create Database Backups

```bash
# Create backup script
cat > backup_database.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/ocr_agent"
mkdir -p $BACKUP_DIR
pg_dump -U ocr_user -d ocr_agent_db | gzip > $BACKUP_DIR/ocr_agent_$(date +%Y%m%d_%H%M%S).sql.gz
find $BACKUP_DIR -type f -mtime +30 -delete  # Keep last 30 days
EOF

chmod +x backup_database.sh

# Add to crontab for daily backups
sudo crontab -e
# Add: 0 2 * * * /var/www/ocr_agent/backup_database.sh
```

---

## Service Configuration

### 1. Systemd Service (Recommended)

Create `/etc/systemd/system/ocr-agent.service`:

```ini
[Unit]
Description=OCR Agent Flask Application
After=network.target postgresql.service redis-server.service
Requires=postgresql.service redis-server.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/ocr_agent
Environment="PATH=/var/www/ocr_agent/venv/bin"
EnvironmentFile=/var/www/ocr_agent/.env
ExecStart=/var/www/ocr_agent/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    --access-logfile /var/log/ocr_agent/access.log \
    --error-logfile /var/log/ocr_agent/error.log \
    --log-level info \
    wsgi:app
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ocr-agent
sudo systemctl start ocr-agent
sudo systemctl status ocr-agent
```

### 2. Celery Task Worker

Create `/etc/systemd/system/ocr-agent-celery.service`:

```ini
[Unit]
Description=OCR Agent Celery Worker
After=network.target redis-server.service
Requires=redis-server.service

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/var/www/ocr_agent
Environment="PATH=/var/www/ocr_agent/venv/bin"
EnvironmentFile=/var/www/ocr_agent/.env
ExecStart=/var/www/ocr_agent/venv/bin/celery -A celery_app worker \
    --loglevel=info \
    --logfile=/var/log/ocr_agent/celery.log
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 3. Nginx Reverse Proxy

Create `/etc/nginx/sites-available/ocr-agent`:

```nginx
upstream ocr_agent {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Logging
    access_log /var/log/nginx/ocr_agent_access.log;
    error_log /var/log/nginx/ocr_agent_error.log;
    
    # Client upload size
    client_max_body_size 500M;
    
    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    
    location / {
        proxy_pass http://ocr_agent;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
    }
    
    # Static files
    location /static/ {
        alias /var/www/ocr_agent/static/;
        expires 30d;
    }
    
    # Upload directory
    location /uploads/ {
        alias /var/www/ocr_agent/uploads/;
        expires 7d;
    }
}
```

Enable Nginx site:
```bash
sudo ln -s /etc/nginx/sites-available/ocr-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Redis Installation

```bash
# Install Redis
sudo apt-get install -y redis-server

# Enable and start Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Configure Redis persistence
sudo nano /etc/redis/redis.conf
# Uncomment: save 900 1
# Uncomment: save 300 10
# Uncomment: save 60 10000
```

---

## Deployment Options

### Option 1: Standalone VM/VPS Deployment

#### Prerequisites:
- Ubuntu 20.04+ or CentOS 8+
- 8GB+ RAM
- 50GB+ storage
- Public IP address

#### Deployment Steps:
1. Follow all installation steps above
2. Configure SSL with Let's Encrypt
3. Set up monitoring and logging
4. Configure firewall rules

#### Firewall Configuration:
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Option 2: Docker Deployment

#### Create Dockerfile:
See `Dockerfile` in project root

#### Create docker-compose.yml:
See `docker-compose.yml` in project root

#### Deploy with Docker:
```bash
# Build and start containers
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Option 3: Kubernetes Deployment

#### Prerequisites:
- Kubernetes cluster (1.20+)
- kubectl configured
- Helm 3+ (optional)

#### Deployment files in `k8s/` directory:
- `k8s/deployment.yaml` - Flask app deployment
- `k8s/service.yaml` - Service definition
- `k8s/ingress.yaml` - Ingress configuration
- `k8s/configmap.yaml` - Configuration management
- `k8s/secret.yaml` - Secrets management
- `k8s/pvc.yaml` - Persistent volumes

#### Deploy:
```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
```

### Option 4: Cloud Platform Deployment

#### AWS Elastic Beanstalk:
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init -p python-3.11 ocr-agent
eb create ocr-agent-prod
eb deploy
```

#### DigitalOcean App Platform:
- Connect GitHub repository
- Configure environment variables
- Set up database
- Deploy

#### Heroku:
```bash
# Login and create app
heroku login
heroku create ocr-agent

# Deploy
git push heroku main
heroku config:set FLASK_ENV=production
```

---

## Testing & Verification

### 1. Application Health Check

```bash
# Check Flask application
curl -X GET http://localhost:5000/health

# Check API endpoints
curl -X GET http://localhost:5000/api/health
curl -X GET http://localhost:5000/api/settings
```

### 2. Database Connection Test

```bash
# Test database connection
psql -U ocr_user -d ocr_agent_db -c "SELECT 1;"

# Check table creation
psql -U ocr_user -d ocr_agent_db -c "\dt"
```

### 3. OnlyOffice Integration Test

```bash
# Test OnlyOffice connectivity
curl -X GET http://localhost:8080/

# Check OnlyOffice health
curl -X GET http://localhost:8080/healthcheck
```

### 4. Run Test Suite

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

### 5. Performance Testing

```bash
# Install locust
pip install locust

# Run load test
locust -f loadtest.py --host=http://localhost:5000
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Error
```
Error: could not connect to server
```
**Solution:**
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Check connection string in .env
# Verify database and user exist
psql -U postgres -c "\l"
```

#### 2. Tesseract Not Found
```
Error: tesseract is not installed
```
**Solution:**
```bash
# Install tesseract
sudo apt-get install -y tesseract-ocr

# Set correct path in .env
TESSERACT_PATH=/usr/bin/tesseract
```

#### 3. Memory Issues
```
Error: MemoryError or Out of Memory
```
**Solution:**
```bash
# Reduce chunk size
CHUNK_SIZE=250
CHUNK_OVERLAP=25

# Reduce worker processes
SERVER_WORKERS=2

# Enable swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 4. Port Already in Use
```
Error: Address already in use
```
**Solution:**
```bash
# Find and kill process using port
sudo lsof -i :5000
sudo kill -9 <PID>
```

#### 5. Permission Denied on Upload
```
Error: Permission denied creating file
```
**Solution:**
```bash
# Fix directory permissions
sudo chown -R www-data:www-data /var/www/ocr_agent/uploads
sudo chmod 755 /var/www/ocr_agent/uploads
```

---

## Security Considerations

### 1. Environment Variables
- Never commit `.env` files to version control
- Use `.env.example` with dummy values
- Rotate secrets regularly
- Use different secrets per environment

### 2. Database Security
```sql
-- Create read-only user for backups
CREATE USER ocr_backup WITH PASSWORD 'backup_password';
GRANT CONNECT ON DATABASE ocr_agent_db TO ocr_backup;
GRANT USAGE ON SCHEMA public TO ocr_backup;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ocr_backup;

-- Enable SSL connections
-- Edit postgresql.conf: ssl = on
```

### 3. Application Security
```python
# In production:
- Set FLASK_DEBUG = False
- Enable CSRF protection
- Use secure session cookies
- Implement rate limiting
- Enable CORS restrictions
```

### 4. SSL/TLS Configuration
```bash
# Install Certbot for Let's Encrypt
sudo apt-get install -y certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### 5. Firewall Rules
```bash
# UFW configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw allow from 10.0.0.0/8 to any port 5432  # Internal DB
sudo ufw enable
```

### 6. Log Management
```bash
# Create log rotation config
sudo nano /etc/logrotate.d/ocr-agent
```

```
/var/log/ocr_agent/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload ocr-agent > /dev/null 2>&1 || true
    endscript
}
```

---

## Monitoring and Maintenance

### 1. System Monitoring
```bash
# Install monitoring tools
sudo apt-get install -y htop iotop nethogs

# Monitor in real-time
htop
```

### 2. Application Monitoring
```bash
# Monitor with systemd
sudo systemctl status ocr-agent
sudo journalctl -u ocr-agent -f

# View logs
tail -f /var/log/ocr_agent/app.log
tail -f /var/log/ocr_agent/error.log
```

### 3. Database Maintenance
```bash
# Regular VACUUM and ANALYZE
sudo -u postgres psql -d ocr_agent_db -c "VACUUM ANALYZE;"

# Check index bloat
sudo -u postgres psql -d ocr_agent_db -c "SELECT * FROM pg_stat_user_indexes;"
```

### 4. Backup Strategy
- Daily automated backups
- Weekly full backups to external storage
- Monthly archival
- Test restore procedures regularly

---

## Support and Documentation

- **GitHub Repository**: https://github.com/yourusername/ocr-agent
- **Documentation**: `/docs` directory
- **Issue Tracker**: GitHub Issues
- **Community**: GitHub Discussions

---

## Version History

- **v1.0.0** - Initial release with basic OCR and chat functionality
- **v1.1.0** - Added OnlyOffice integration
- **v1.2.0** - Added DeepSeek OCR support
- **v1.3.0** - Multi-language support (French, Cameroon Education)

---

**Last Updated**: November 1, 2025
**Maintainer**: [Your Name/Organization]
