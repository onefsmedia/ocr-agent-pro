# OCR Agent - Panel 7 Podman Deployment Guide

## 🚀 Quick Deployment

### Prerequisites
1. **Podman Desktop** installed and running
2. **OpenAI API Key** for lesson generation (optional)
3. **8GB+ RAM** recommended

### One-Click Deployment

```powershell
# Run the deployment script
.\deploy-podman.ps1
```

### Manual Deployment

```powershell
# 1. Copy environment file
Copy-Item ".env.production" ".env"

# 2. Start all services
podman-compose up -d --build

# 3. Wait for startup
Start-Sleep 30

# 4. Check status
podman-compose ps
```

## 🔧 Configuration

### Environment Variables (.env.production)
- `OPENAI_API_KEY`: Required for Panel 7 lesson generation
- `ONLYOFFICE_URL`: OnlyOffice server URL (default: http://onlyoffice_server)
- `DATABASE_URL`: PostgreSQL connection string
- `USE_DEEPSEEK_OCR`: Enable/disable DeepSeek OCR

### Service Ports
- **OCR Agent**: 5000 (main application)
- **OnlyOffice**: 8000 (document server)
- **PostgreSQL**: 5432 (database)
- **Redis**: 6379 (cache/queue)
- **Ollama**: 11434 (local LLM)

## 📊 Service Status

Check service health:
```powershell
# View all services
podman-compose ps

# Check specific service logs
podman-compose logs -f ocr_agent
podman-compose logs -f onlyoffice
```

## 🎓 Panel 7 Usage

1. **Access Dashboard**: http://localhost:5000
2. **Navigate to Panel 7**: Click "Generate Lessons"
3. **Configure OnlyOffice**: Check server status in Panel 7
4. **Upload Curriculum**: Use Panel 1 to upload curriculum documents
5. **Generate Lessons**: Select subject/class and generate AI-powered lesson notes

### Panel 7 Features
- ✅ AI lesson note generation
- ✅ OnlyOffice document creation
- ✅ Subject-specific content
- ✅ Batch lesson generation
- ✅ Real-time progress tracking

## 🛠️ Management

### Update Application
```powershell
# Pull latest changes and rebuild
git pull
podman-compose up -d --build
```

### Backup Database
```powershell
# Create database backup
podman exec ocr_postgres pg_dump -U renderman ocr_agent > backup.sql
```

### Scale Services
```powershell
# Scale OCR agent instances
podman-compose up -d --scale ocr_agent=3
```

## 🔍 Troubleshooting

### Common Issues

**OnlyOffice Not Starting**
```powershell
# Check OnlyOffice logs
podman-compose logs onlyoffice

# Restart OnlyOffice
podman-compose restart onlyoffice
```

**Database Connection Failed**
```powershell
# Check PostgreSQL status
podman-compose logs postgres

# Reset database
podman-compose down
podman volume rm ocr_postgres_data
podman-compose up -d
```

**Lesson Generation Fails**
- Check OpenAI API key in `.env`
- Verify curriculum documents uploaded
- Check OCR agent logs for AI errors

### Performance Optimization

**For Better Performance:**
1. Allocate more RAM to Podman
2. Use SSD storage for volumes
3. Enable GPU support for Ollama
4. Scale worker processes

**Resource Usage:**
- **Light Load**: 4GB RAM, 2 CPU cores
- **Medium Load**: 8GB RAM, 4 CPU cores  
- **Heavy Load**: 16GB RAM, 8+ CPU cores

## 📁 Data Persistence

All data is stored in Docker volumes:
- `postgres_data`: Database files
- `onlyoffice_data`: OnlyOffice documents
- `ollama_data`: Local LLM models

## 🚀 Production Deployment

For production use:
1. Change default passwords
2. Enable SSL/TLS
3. Use external database
4. Configure backup strategy
5. Set up monitoring

---

**🎉 Your enhanced 7-panel OCR Agent with lesson generation is ready to use!**