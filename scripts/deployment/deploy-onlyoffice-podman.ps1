# OnlyOffice Document Server Deployment Script for Podman
# This script sets up OnlyOffice Document Server for the OCR Agent using Podman

Write-Host "Starting OnlyOffice Document Server for OCR Agent using Podman..." -ForegroundColor Green

# Check if Podman is available
try {
    podman --version | Out-Null
    Write-Host "Podman is available" -ForegroundColor Green
} catch {
    Write-Host "Podman is not available. Please install Podman first." -ForegroundColor Red
    exit 1
}

# Stop and remove existing OnlyOffice containers if any
Write-Host "Stopping existing OnlyOffice containers..." -ForegroundColor Yellow
podman stop onlyoffice-documentserver 2>$null
podman stop onlyoffice-redis 2>$null
podman stop onlyoffice-rabbitmq 2>$null

Write-Host "Removing existing containers..." -ForegroundColor Yellow
podman rm onlyoffice-documentserver 2>$null
podman rm onlyoffice-redis 2>$null
podman rm onlyoffice-rabbitmq 2>$null

# Pull the latest OnlyOffice image
Write-Host "Pulling OnlyOffice Document Server image..." -ForegroundColor Yellow
podman pull docker.io/onlyoffice/documentserver:latest

# Create a pod for OnlyOffice services
Write-Host "Creating OnlyOffice pod..." -ForegroundColor Yellow
podman pod rm onlyoffice-pod 2>$null
podman pod create --name onlyoffice-pod -p 8000:80 -p 6379:6379 -p 5672:5672 -p 15672:15672

# Start Redis container
Write-Host "Starting Redis container..." -ForegroundColor Yellow
podman run -d --name onlyoffice-redis --pod onlyoffice-pod redis:7-alpine

# Start OnlyOffice Document Server
Write-Host "Starting OnlyOffice Document Server..." -ForegroundColor Yellow
podman run -d --name onlyoffice-documentserver --pod onlyoffice-pod `
    -e JWT_ENABLED=true `
    -e JWT_SECRET=ocr-agent-secret-key-2025 `
    -e JWT_HEADER=Authorization `
    -e JWT_IN_BODY=true `
    docker.io/onlyoffice/documentserver:latest

# Wait for services to start
Write-Host "Waiting for OnlyOffice to initialize (this may take 2-3 minutes)..." -ForegroundColor Yellow
$timeout = 180  # 3 minutes timeout
$elapsed = 0

do {
    Start-Sleep -Seconds 10
    $elapsed += 10
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/healthcheck" -UseBasicParsing -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "OnlyOffice Document Server is running!" -ForegroundColor Green
            break
        }
    } catch {
        Write-Host "Still waiting for OnlyOffice to start... ($elapsed/$timeout seconds)" -ForegroundColor Yellow
    }
    
    if ($elapsed -ge $timeout) {
        Write-Host "Timeout waiting for OnlyOffice to start" -ForegroundColor Red
        Write-Host "You can check the logs with: podman logs onlyoffice-documentserver" -ForegroundColor Yellow
        break
    }
} while ($true)

# Display service information
Write-Host ""
Write-Host "OnlyOffice Service Information:" -ForegroundColor Cyan
Write-Host "Document Server: http://localhost:8000" -ForegroundColor White
Write-Host "Redis Cache: localhost:6379" -ForegroundColor White
Write-Host "JWT Secret: ocr-agent-secret-key-2025" -ForegroundColor White

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Update OCR Agent settings with OnlyOffice URL: http://localhost:8000" -ForegroundColor White
Write-Host "2. Set JWT Secret: ocr-agent-secret-key-2025" -ForegroundColor White
Write-Host "3. Test the connection in the OCR Agent settings panel" -ForegroundColor White

Write-Host ""
Write-Host "OnlyOffice deployment complete!" -ForegroundColor Green

# Show container status
Write-Host ""
Write-Host "Container Status:" -ForegroundColor Cyan
podman ps --pod