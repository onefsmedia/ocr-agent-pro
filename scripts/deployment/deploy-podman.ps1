# OCR Agent - Podman Desktop Deployment Script
# PowerShell version for Windows

Write-Host "🐘 OCR Agent - Podman Desktop Deployment" -ForegroundColor Blue
Write-Host "=========================================" -ForegroundColor Blue
Write-Host ""

# Check if Podman is installed
try {
    $podmanVersion = podman --version
    Write-Host "✅ Podman found: $podmanVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Podman is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Podman Desktop from: https://podman-desktop.io/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check if docker-compose.yml exists
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "❌ docker-compose.yml not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the OCR Agent root directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ docker-compose.yml found" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Starting OCR Agent deployment..." -ForegroundColor Cyan
Write-Host ""

# Stop any existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
try {
    podman-compose down 2>$null
} catch {
    # Ignore errors if no containers are running
}

Write-Host ""
Write-Host "🔨 Building and starting services..." -ForegroundColor Cyan

# Copy production environment
Copy-Item ".env.production" ".env" -Force -ErrorAction SilentlyContinue
Write-Host "✅ Production environment loaded" -ForegroundColor Green

try {
    podman-compose up -d --build
    
    if ($LASTEXITCODE -ne 0) {
        throw "Deployment failed"
    }
} catch {
    Write-Host ""
    Write-Host "❌ Deployment failed! Check the logs above for errors." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "- Make sure Podman Desktop is running" -ForegroundColor Yellow
    Write-Host "- Check if ports 5000, 5432, 6379 are available" -ForegroundColor Yellow
    Write-Host "- Verify docker-compose.yml syntax" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "📊 Checking service status..." -ForegroundColor Cyan
podman-compose ps

Write-Host ""
Write-Host "✅ OCR Agent deployed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your application at:" -ForegroundColor Cyan
Write-Host "   ➤ Web Interface: http://localhost:5000" -ForegroundColor White
Write-Host "   ➤ OnlyOffice Server: http://localhost:8000" -ForegroundColor White
Write-Host "   ➤ PostgreSQL: localhost:5432 (user: renderman, password: Master@2025)" -ForegroundColor White
Write-Host "   ➤ Redis: localhost:6379" -ForegroundColor White
Write-Host "   ➤ Ollama LLM: http://localhost:11434" -ForegroundColor White
Write-Host ""
Write-Host "🎓 New Panel 7 Features:" -ForegroundColor Green
Write-Host "   ➤ AI-Powered Lesson Generation" -ForegroundColor White
Write-Host "   ➤ OnlyOffice Document Integration" -ForegroundColor White
Write-Host "   ➤ Curriculum-Based Content Creation" -ForegroundColor White
Write-Host "   ➤ Multi-Subject Support" -ForegroundColor White
Write-Host ""
Write-Host "📝 Useful commands:" -ForegroundColor Cyan
Write-Host "   ➤ View logs: podman-compose logs -f ocr_agent" -ForegroundColor White
Write-Host "   ➤ Check status: podman-compose ps" -ForegroundColor White
Write-Host "   ➤ Stop services: podman-compose down" -ForegroundColor White
Write-Host "   ➤ Update app: podman-compose up -d --build" -ForegroundColor White
Write-Host ""
Write-Host "📚 For detailed documentation, see DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host ""

# Try to open the web browser
Write-Host "🌍 Opening web browser..." -ForegroundColor Yellow
try {
    Start-Process "http://localhost:5000"
} catch {
    Write-Host "Could not open browser automatically. Please navigate to http://localhost:5000" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"