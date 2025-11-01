# OCR Agent - Podman/Docker Compose Configuration

## Development Setup

### Prerequisites
- Docker or Podman with compose support
- 4GB+ RAM recommended
- 10GB+ disk space

### Quick Start

1. **Clone and Setup**:
```bash
git clone <repository>
cd ocr-agent
cp .env.example .env
# Edit .env with your configuration
```

2. **Start Services**:
```bash
# Using Docker
docker-compose up -d

# Using Podman
podman-compose up -d
```

3. **Initialize Database**:
```bash
# Wait for services to start, then initialize
docker-compose exec ocr_agent python app.py init-db

# Or with Podman
podman-compose exec ocr_agent python app.py init-db
```

4. **Access Application**:
- Web Interface: http://localhost:5000
- API Documentation: http://localhost:5000/api
- Ollama LLM: http://localhost:11434

### Service Architecture

- **ocr_agent**: Main Flask application (Port 5000)
- **postgres**: PostgreSQL with pgvector (Port 5432)
- **redis**: Redis for background tasks (Port 6379)
- **celery_worker**: Background OCR processing
- **ollama**: Local LLM server (Port 11434)
- **nginx**: Reverse proxy (Port 80/443) - Production only

### Configuration

#### Environment Variables (.env)
```bash
# Database
DATABASE_URL=postgresql://ocr_user:ocr_password@postgres:5432/ocr_agent

# Security
SECRET_KEY=your-secret-key-here

# OCR Settings
TESSERACT_PATH=/usr/bin/tesseract
USE_DEEPSEEK_OCR=true
DEEPSEEK_OCR_URL=http://deepseek-ocr:8001

# AI/LLM
DEFAULT_LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://ollama:11434
OPENAI_API_KEY=your-openai-key

# OnlyOffice Integration
ONLYOFFICE_URL=http://onlyoffice:8000
ONLYOFFICE_SECRET=your-onlyoffice-secret
ONLYOFFICE_TOKEN=your-onlyoffice-token
ONLYOFFICE_STORAGE_URL=http://localhost:5000/storage
```

#### Volume Mounts
- `./uploads:/app/uploads` - Document storage
- `./logs:/app/logs` - Application logs
- `postgres_data` - Database persistence
- `ollama_data` - LLM models storage

### Development vs Production

#### Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f ocr_agent

# Stop services
docker-compose down
```

#### Production
```bash
# Start with Nginx proxy
docker-compose --profile production up -d

# With SSL (configure certificates first)
# Copy SSL certificates to ./docker/ssl/
docker-compose --profile production up -d
```

### GPU Support (Optional)

For GPU-accelerated LLM inference with Ollama:

1. **Install NVIDIA Container Toolkit**
2. **Uncomment GPU configuration** in docker-compose.yml
3. **Start services**:
```bash
docker-compose up -d
```

For CPU-only deployment, the default configuration works without modifications.

### Scaling and Performance

#### Horizontal Scaling
```bash
# Scale Celery workers
docker-compose up -d --scale celery_worker=3

# Scale main app (with load balancer)
docker-compose up -d --scale ocr_agent=2
```

#### Resource Limits
Add to docker-compose.yml services:
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G
    reservations:
      cpus: '1.0'
      memory: 2G
```

### Monitoring and Logging

#### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs ocr_agent

# Follow logs
docker-compose logs -f
```

#### Health Checks
```bash
# Check service health
docker-compose ps

# Manual health check
curl http://localhost:5000/health
```

### Backup and Restore

#### Database Backup
```bash
docker-compose exec postgres pg_dump -U ocr_user ocr_agent > backup.sql
```

#### Database Restore
```bash
docker-compose exec -T postgres psql -U ocr_user ocr_agent < backup.sql
```

#### Volume Backup
```bash
# Backup uploads
docker run --rm -v ocr_agent_uploads:/data -v $(pwd):/backup alpine tar czf /backup/uploads.tar.gz /data

# Backup database
docker run --rm -v ocr_agent_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres.tar.gz /data
```

### Troubleshooting

#### Common Issues

1. **Port Conflicts**:
```bash
# Check port usage
netstat -tulpn | grep :5000

# Change ports in docker-compose.yml if needed
```

2. **Permission Errors**:
```bash
# Fix upload directory permissions
sudo chown -R 1000:1000 uploads/
```

3. **Database Connection Issues**:
```bash
# Check PostgreSQL status
docker-compose exec postgres pg_isready -U ocr_user

# Reset database
docker-compose down -v
docker-compose up -d postgres
# Wait, then initialize
```

4. **OCR Processing Fails**:
```bash
# Check Tesseract installation
docker-compose exec ocr_agent tesseract --version

# Check worker logs
docker-compose logs celery_worker
```

5. **LLM Connection Issues**:
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Pull a model
docker-compose exec ollama ollama pull llama2
```

### Security Considerations

#### Production Deployment
- Change default passwords and secrets
- Configure SSL/TLS certificates
- Set up firewall rules
- Enable audit logging
- Regular security updates

#### Network Security
```bash
# Create isolated network
docker network create ocr_secure_network

# Update docker-compose.yml to use custom network
```

#### Data Protection
- Encrypt sensitive data
- Regular backups
- Access controls
- Data retention policies

### Advanced Configuration

#### Custom Models
```bash
# Download custom Ollama model
docker-compose exec ollama ollama pull mistral

# Configure in environment
DEFAULT_LLM_MODEL=mistral
```

#### Google Cloud Integration
1. Enable Google Cloud APIs
2. Create service account
3. Download credentials JSON
4. Mount credentials file:
```yaml
volumes:
  - ./google-credentials.json:/app/google-credentials.json
environment:
  - GOOGLE_APPLICATION_CREDENTIALS=/app/google-credentials.json
```

#### Custom OCR Models
```bash
# Add custom Tesseract language packs
# In Dockerfile:
RUN apt-get install tesseract-ocr-fra tesseract-ocr-deu
```

This setup provides a complete, scalable OCR application with AI capabilities that can run on both desktop and cloud environments using Docker or Podman.