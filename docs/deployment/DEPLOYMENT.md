# 🐘 OCR Agent - Podman Desktop Deployment Guide

## 📋 Prerequisites

1. **Podman Desktop** installed and running
2. **Local AI Services** (optional but recommended):
   - Ollama running on `http://localhost:11434`
   - LM Studio running on `http://localhost:1234`

## 🚀 Quick Deployment

### Step 1: Build and Deploy with Podman Desktop

1. Open **Podman Desktop**
2. Navigate to **Containers** → **Compose**
3. Click **Create from compose file**
4. Select the `docker-compose.yml` file from this directory
5. Click **Deploy**

### Step 2: Alternative - Command Line Deployment

```bash
# Navigate to the OCR Agent directory
cd "c:\OCR Agent"

# Build and start all services
podman-compose up -d --build

# Check service status
podman-compose ps

# View logs
podman-compose logs -f ocr_agent
```

## 🌐 Access Points

- **OCR Agent Web Interface**: http://localhost:5000
- **PostgreSQL Database**: localhost:5432
- **Redis Cache**: localhost:6379

## 🔐 Default Credentials

### PostgreSQL Database
- **Host**: localhost:5432
- **Database**: ocr_agent
- **Username**: renderman
- **Password**: Master@2025

### Application Access
- **No authentication required** (can be added later)
- Direct access to all 6 dashboard panels

## 📱 Application Features

### Panel 1: Document Ingestion
- Upload PDF and image files
- Automatic OCR processing with Tesseract
- Text extraction and chunking

### Panel 2: Table View  
- View all processed documents
- Browse extracted text chunks
- Document metadata and status

### Panel 3: System Settings
- **Database Tab**: Connection settings and status
- **OCR Tab**: Tesseract and DeepSeek OCR configuration
- **OnlyOffice Tab**: Integration settings
- **AI/LLM Tab**: Configure Ollama, LM Studio, OpenAI
- **System Tab**: General application settings

### Panel 4: Database Status
- Real-time PostgreSQL connection monitoring
- Database statistics and health metrics
- Performance indicators

### Panel 5: AI Chatbot
- Interactive query interface
- RAG (Retrieval Augmented Generation)
- Multiple LLM provider support
- Document-based question answering

### Panel 6: Prompt Management
- Configure system prompts
- Custom AI behavior settings
- Template management

## 🛠️ Configuration Options

### Environment Variables

The application supports these key environment variables:

```bash
# Database
DATABASE_URL=postgresql://renderman:Master@2025@postgres:5432/ocr_agent

# AI Services
OLLAMA_BASE_URL=http://host.containers.internal:11434
LM_STUDIO_BASE_URL=http://host.containers.internal:1234
OPENAI_API_KEY=your-openai-key

# OCR Settings
TESSERACT_PATH=/usr/bin/tesseract
USE_DEEPSEEK_OCR=false

# OnlyOffice Integration
ONLYOFFICE_URL=http://onlyoffice:8000
ONLYOFFICE_SECRET=your-secret
```

### Connecting to Local AI Services

The application is configured to connect to AI services running on your host machine:

1. **Ollama**: Make sure Ollama is running and accessible at `http://localhost:11434`
2. **LM Studio**: Ensure LM Studio API server is running on `http://localhost:1234`
3. **OpenAI**: Add your API key to the environment variables

## 🔧 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL container logs
podman logs ocr_postgres

# Test database connection
podman exec -it ocr_postgres psql -U renderman -d ocr_agent -c "\l"
```

### Application Logs
```bash
# View OCR Agent logs
podman logs -f ocr_agent_app

# Check health status
curl http://localhost:5000/api/health
```

### Container Status
```bash
# Check all containers
podman-compose ps

# Restart services
podman-compose restart ocr_agent

# Rebuild if needed
podman-compose up -d --build --force-recreate
```

## 🗂️ Data Persistence

- **PostgreSQL Data**: Stored in `postgres_data` volume
- **Uploaded Files**: Stored in `./uploads` directory
- **Application Logs**: Stored in `./logs` directory
- **Redis Cache**: Stored in `redis_data` volume

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
podman-compose up -d --build
```

### Database Backup
```bash
# Backup database
podman exec ocr_postgres pg_dump -U renderman ocr_agent > backup_$(date +%Y%m%d).sql

# Restore database
podman exec -i ocr_postgres psql -U renderman ocr_agent < backup_20231023.sql
```

### Clean Up
```bash
# Stop all services
podman-compose down

# Remove volumes (CAUTION: This will delete all data)
podman-compose down -v

# Remove images
podman rmi ocr-agent_ocr_agent
```

## 🚀 Production Considerations

For production deployment, consider:

1. **Security**: Change default passwords and add authentication
2. **SSL/TLS**: Add reverse proxy with SSL certificates
3. **Monitoring**: Add logging and monitoring solutions
4. **Backup**: Implement automated database backups
5. **Scaling**: Consider load balancing for multiple instances

## 📞 Support

- Check logs first: `podman-compose logs -f`
- Health check endpoint: `http://localhost:5000/api/health`
- Database status: Access Panel 4 in the web interface

---

## 📚 Additional Resources

### Local Development

If you want to run locally without containers:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies (Windows with Chocolatey)
choco install tesseract

# Set environment variables
$env:DATABASE_URL="postgresql://renderman:Master@2025@localhost:5432/ocr_agent"
$env:FLASK_ENV="development"

# Run application
python app.py
```

### OnlyOffice Integration

To enable OnlyOffice document editing:

1. Deploy OnlyOffice Document Server
2. Configure the URL and secret in Panel 3
3. Upload documents through Panel 1
4. Edit documents directly in the interface

### AI Service Configuration

The application supports multiple AI providers:

- **Ollama**: Local models with privacy
- **LM Studio**: Local model server
- **OpenAI**: Cloud-based GPT models
- **Custom**: Add your own provider endpoints

Enable and start:
```bash
sudo systemctl enable ocr-agent
sudo systemctl start ocr-agent
```

### Cloud Deployment

#### AWS EC2
1. Launch EC2 instance (t3.medium or larger)
2. Install dependencies
3. Configure RDS PostgreSQL with pgvector
4. Deploy application
5. Configure ALB/ELB

#### Google Cloud Platform
1. Create Compute Engine instance
2. Use Cloud SQL for PostgreSQL
3. Configure Cloud Storage for file uploads
4. Deploy with Cloud Run (containerized)

#### Azure
1. Create Azure VM
2. Use Azure Database for PostgreSQL
3. Configure Azure Blob Storage
4. Deploy with Azure Container Instances

### Security Considerations

1. **Environment Variables**:
   - Never commit secrets to version control
   - Use environment-specific configurations
   - Rotate secrets regularly

2. **Database Security**:
   - Use strong passwords
   - Enable SSL connections
   - Restrict network access

3. **File Upload Security**:
   - Validate file types and sizes
   - Scan for malware
   - Use secure file storage

4. **API Security**:
   - Implement rate limiting
   - Use HTTPS only
   - Validate all inputs

### Monitoring and Maintenance

1. **Logging**:
   - Configure structured logging
   - Monitor application logs
   - Set up log rotation

2. **Metrics**:
   - Monitor CPU, memory usage
   - Track API response times
   - Monitor database performance

3. **Backups**:
   - Regular database backups
   - File upload backups
   - Test restore procedures

4. **Updates**:
   - Regular dependency updates
   - Security patches
   - Monitor for vulnerabilities