# OCR Agent Podman Deployment Script
# This script deploys the OCR Agent without requiring external image downloads

Write-Host "Starting OCR Agent deployment with Podman..." -ForegroundColor Green

# Create network
Write-Host "Creating OCR network..." -ForegroundColor Yellow
podman network create ocr_network 2>$null

# Create volumes
Write-Host "Creating volumes..." -ForegroundColor Yellow
podman volume create postgres_data 2>$null
podman volume create onlyoffice_data 2>$null
podman volume create ollama_data 2>$null

# Check if we have cached images
$images = @("postgres:16", "redis:7-alpine", "onlyoffice/documentserver:latest")

foreach ($image in $images) {
    Write-Host "Checking for image: $image" -ForegroundColor Cyan
    $result = podman images --filter "reference=$image" --format "{{.Repository}}:{{.Tag}}"
    if (-not $result) {
        Write-Host "Image $image not found locally. Attempting to pull..." -ForegroundColor Yellow
        try {
            podman pull $image
            Write-Host "Successfully pulled $image" -ForegroundColor Green
        }
        catch {
            Write-Host "Failed to pull $image. Skipping..." -ForegroundColor Red
        }
    } else {
        Write-Host "Found cached image: $image" -ForegroundColor Green
    }
}

# Build our application containers
Write-Host "Building OCR Agent application..." -ForegroundColor Yellow
podman build -t ocr-agent:latest . 

Write-Host "Building DeepSeek OCR service..." -ForegroundColor Yellow
podman build -t deepseek-ocr:latest ./docker/deepseek-ocr/

Write-Host "Deployment preparation complete!" -ForegroundColor Green
Write-Host "To start services, run: podman-compose up -d" -ForegroundColor Cyan