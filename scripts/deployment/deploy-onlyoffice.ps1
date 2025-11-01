# OnlyOffice Document Server Deployment Script
# This script sets up OnlyOffice Document Server for the OCR Agent

Write-Host "Starting OnlyOffice Document Server for OCR Agent..." -ForegroundColor Green

# Check if Docker is available
try {
    docker --version | Out-Null
    Write-Host "Docker is available" -ForegroundColor Green
} catch {
    Write-Host "Docker is not available. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Stop existing OnlyOffice containers if any
Write-Host "Stopping existing OnlyOffice containers..." -ForegroundColor Yellow
docker stop onlyoffice-documentserver 2>$null
docker stop onlyoffice-redis 2>$null
docker stop onlyoffice-rabbitmq 2>$null

# Remove existing containers
Write-Host "Removing existing containers..." -ForegroundColor Yellow
docker rm onlyoffice-documentserver 2>$null
docker rm onlyoffice-redis 2>$null
docker rm onlyoffice-rabbitmq 2>$null

# Pull the latest OnlyOffice image
Write-Host "Pulling OnlyOffice Document Server image..." -ForegroundColor Yellow
docker pull onlyoffice/documentserver:latest

# Start OnlyOffice Document Server using Docker Compose
Write-Host "Starting OnlyOffice services..." -ForegroundColor Yellow
docker-compose -f docker-compose.onlyoffice.yml up -d

# Wait for services to start
Write-Host "Waiting for OnlyOffice to initialize (this may take 2-3 minutes)..." -ForegroundColor Yellow
$timeout = 180  # 3 minutes timeout
$elapsed = 0

do {
    Start-Sleep -Seconds 10
    $elapsed += 10
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/healthcheck" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "OnlyOffice Document Server is running!" -ForegroundColor Green
            break
        }
    } catch {
        Write-Host "Still waiting for OnlyOffice to start... ($elapsed/$timeout seconds)" -ForegroundColor Yellow
    }
    
    if ($elapsed -ge $timeout) {
        Write-Host "Timeout waiting for OnlyOffice to start" -ForegroundColor Red
        Write-Host "You can check the logs with: docker logs onlyoffice-documentserver" -ForegroundColor Yellow
        break
    }
} while ($true)

# Display service information
Write-Host ""
Write-Host "OnlyOffice Service Information:" -ForegroundColor Cyan
Write-Host "Document Server: http://localhost:8000" -ForegroundColor White
Write-Host "Redis Cache: localhost:6379" -ForegroundColor White
Write-Host "RabbitMQ Management: http://localhost:15672 (onlyoffice/onlyoffice2025)" -ForegroundColor White
Write-Host "JWT Secret: ocr-agent-secret-key-2025" -ForegroundColor White

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Update OCR Agent settings with OnlyOffice URL: http://localhost:8000" -ForegroundColor White
Write-Host "2. Set JWT Secret: ocr-agent-secret-key-2025" -ForegroundColor White
Write-Host "3. Test the connection in the OCR Agent settings panel" -ForegroundColor White

Write-Host ""
Write-Host "OnlyOffice deployment complete!" -ForegroundColor Green