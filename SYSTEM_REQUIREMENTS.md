# System Requirements & Installation Guide - OCR Agent Pro v1.3.0

**Complete hardware, software, and installation requirements**

---

## 📋 Table of Contents

1. [Hardware Requirements](#hardware-requirements)
2. [Software Requirements](#software-requirements)
3. [GPU Requirements (Optional)](#gpu-requirements-optional)
4. [Python Packages](#python-packages)
5. [System Dependencies](#system-dependencies)
6. [Installation Commands](#installation-commands)
7. [Post-Installation Verification](#post-installation-verification)

---

## 💻 Hardware Requirements

### Minimum Configuration (Development/Testing)

**CPU:**
- 4 cores / 8 threads minimum
- x86_64 architecture (Intel/AMD)
- Recommended: Intel i5/i7 or AMD Ryzen 5/7

**RAM:**
- 8GB minimum
- 16GB recommended
- 32GB for production with large documents

**Storage:**
- **50GB free space minimum**
  - 10GB for application and dependencies
  - 20GB for document uploads
  - 10GB for vector embeddings/models
  - 10GB for logs and temporary files
- **SSD strongly recommended** for database and embeddings
- Additional space for document storage (varies by usage)

**Network:**
- 100 Mbps minimum
- 1 Gbps recommended for production

### Recommended Configuration (Production)

**CPU:**
- 8+ cores / 16+ threads
- Intel Xeon or AMD EPYC for servers
- High clock speed (3.0+ GHz)

**RAM:**
- 32GB minimum
- 64GB+ recommended
- 128GB for heavy workloads (500MB+ documents)

**Storage:**
- **200GB+ NVMe SSD** for application and database
- Separate drive for document storage (1TB+)
- RAID configuration recommended for data redundancy

**Network:**
- 1 Gbps minimum
- 10 Gbps for high-traffic deployments
- Low latency (<5ms to database)

---

## 🎮 GPU Requirements (Optional)

GPU acceleration is **optional** but provides **significant performance improvements** for:
- AI/LLM inference (Ollama with GPU)
- DeepSeek OCR processing
- Vector embedding generation (large batches)

### NVIDIA GPU (Recommended)

**Minimum GPU:**
- NVIDIA GTX 1060 (6GB VRAM)
- CUDA Compute Capability 6.0+

**Recommended GPU:**
- NVIDIA RTX 3060 (12GB VRAM) or better
- NVIDIA RTX 4080/4090 for production
- NVIDIA A100/H100 for enterprise

**GPU Memory (VRAM):**
- **6GB minimum** - Small models (7B parameters)
- **12GB recommended** - Medium models (13B parameters)
- **24GB+ optimal** - Large models (70B+ parameters)

**CUDA Version:**
- CUDA 11.8 or 12.0+
- cuDNN 8.x
- NVIDIA Driver 525.x or newer

### AMD GPU (Experimental)

**Supported:**
- AMD Radeon RX 6000/7000 series
- ROCm 5.4+ (Linux only)
- 8GB+ VRAM

**Note:** AMD GPU support is experimental. NVIDIA is recommended for production.

### Apple Silicon (M1/M2/M3)

**Supported:**
- Apple M1/M2/M3 chips
- Metal Performance Shaders (MPS)
- 16GB+ unified memory recommended

**Performance:** Good for inference, excellent power efficiency

---

## 🖥️ Software Requirements

### Operating Systems

#### Linux (Recommended for Production)

**Supported Distributions:**
- **Ubuntu 20.04 LTS / 22.04 LTS** ✅ Recommended
- **Debian 11/12**
- **CentOS Stream 8/9**
- **RHEL 8/9**
- **Rocky Linux 8/9**
- **Fedora 37+**

**Kernel:** 5.4+ (5.15+ recommended)

#### Windows

**Supported Versions:**
- **Windows 10** (21H2 or later)
- **Windows 11**
- **Windows Server 2019**
- **Windows Server 2022** ✅ Recommended for production

**Build:** 19041+ minimum

#### macOS

**Supported Versions:**
- **macOS 12 (Monterey)**
- **macOS 13 (Ventura)**
- **macOS 14 (Sonoma)** ✅ Recommended

**Architecture:** Intel x86_64 or Apple Silicon (ARM64)

---

## 🐍 Python Requirements

### Python Version

**Required:** Python 3.11.0 or higher
**Recommended:** Python 3.11.6+

**Installation:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# CentOS/RHEL
sudo dnf install python3.11 python3.11-devel

# Windows
# Download from: https://www.python.org/downloads/
# Or use: winget install Python.Python.3.11

# macOS
brew install python@3.11
```

### Python Packages (from requirements.txt)

**Core Framework:**
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.0.5
- Flask-CORS 4.0.0
- python-dotenv 1.0.0

**Database:**
- psycopg2-binary 2.9.9 (PostgreSQL driver)
- pgvector 0.2.4 (Vector similarity search)

**OCR & Image Processing:**
- pytesseract 0.3.10
- pdf2image 1.16.3
- Pillow 10.1.0
- PyPDF2 3.0.1

**AI/LLM:**
- openai 1.3.7
- langchain 0.1.0
- langchain-community 0.0.10
- sentence-transformers 2.2.2

**Vector Embeddings:**
- sentence-transformers 2.2.2
- numpy 1.24.3
- torch 2.0+ (installed with sentence-transformers)

**Web Server:**
- gunicorn 21.2.0 (Linux/macOS)
- waitress 2.1.2 (Windows)
- Werkzeug 3.0.1

**Background Tasks:**
- celery 5.3.4
- redis 5.0.1

**Security:**
- cryptography 41.0.7
- PyJWT 2.8.0

**Utilities:**
- requests 2.31.0
- httpx 0.25.2
- python-multipart 0.0.6
- python-json-logger 2.0.7

### Installation Command

```bash
# Create virtual environment
python3.11 -m venv .venv

# Activate virtual environment
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install all packages
pip install -r requirements.txt
```

---

## 📦 System Dependencies

### PostgreSQL Database

**Version:** PostgreSQL 12 or higher
**Recommended:** PostgreSQL 14 or 16

**Extensions Required:**
- **pgvector** - Vector similarity search
- **uuid-ossp** - UUID generation
- **pg_trgm** - Text search (optional)

**Installation:**

```bash
# Ubuntu/Debian
sudo apt install postgresql-14 postgresql-contrib-14
sudo apt install postgresql-14-pgvector

# CentOS/RHEL
sudo dnf install postgresql14-server postgresql14-contrib
# pgvector: build from source or use PGDG repository

# macOS
brew install postgresql@14
brew install pgvector

# Windows
# Download from: https://www.postgresql.org/download/windows/
# pgvector: https://github.com/pgvector/pgvector/releases
```

### Tesseract OCR

**Version:** Tesseract 4.0 or higher
**Recommended:** Tesseract 5.3+

**Languages Needed:**
- eng (English) - Required
- fra (French) - Optional
- deu (German) - Optional
- spa (Spanish) - Optional

**Installation:**

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr tesseract-ocr-eng
# Additional languages:
sudo apt install tesseract-ocr-fra tesseract-ocr-deu tesseract-ocr-spa

# CentOS/RHEL
sudo dnf install tesseract tesseract-langpack-eng

# macOS
brew install tesseract
brew install tesseract-lang  # All languages

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Or use: choco install tesseract
```

### Poppler Utils (PDF Processing)

**Required for:** PDF to image conversion

**Installation:**

```bash
# Ubuntu/Debian
sudo apt install poppler-utils

# CentOS/RHEL
sudo dnf install poppler-utils

# macOS
brew install poppler

# Windows
# Download from: https://blog.alivate.com.au/poppler-windows/
# Or included with Anaconda
```

### Redis (Optional - for caching and background tasks)

**Version:** Redis 6.0 or higher
**Recommended:** Redis 7.0+

**Installation:**

```bash
# Ubuntu/Debian
sudo apt install redis-server

# CentOS/RHEL
sudo dnf install redis

# macOS
brew install redis

# Windows
# Download from: https://github.com/microsoftarchive/redis/releases
# Or use Docker: docker run -d -p 6379:6379 redis:7-alpine
```

### Build Tools (for compiling Python packages)

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev libpq-dev

# CentOS/RHEL
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel postgresql-devel
```

**Windows:**
- Microsoft Visual C++ 14.0+ (Visual Studio Build Tools)
- Download: https://visualstudio.microsoft.com/downloads/

**macOS:**
```bash
xcode-select --install
```

---

## 🚀 Installation Commands by Operating System

### Ubuntu/Debian (Complete Installation)

```bash
#!/bin/bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Install PostgreSQL with pgvector
sudo apt install -y postgresql-14 postgresql-contrib-14
sudo apt install -y postgresql-14-pgvector

# Install Tesseract OCR
sudo apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-fra

# Install Poppler
sudo apt install -y poppler-utils

# Install Redis
sudo apt install -y redis-server

# Install build tools
sudo apt install -y build-essential libpq-dev

# Install Git
sudo apt install -y git

# Clone repository
git clone https://github.com/onefsmedia/ocr-agent-pro.git
cd ocr-agent-pro

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Setup database
python scripts/setup/setup_database.py

# Start application
python server.py
```

### CentOS/RHEL (Complete Installation)

```bash
#!/bin/bash
# Update system
sudo dnf update -y

# Install Python 3.11
sudo dnf install -y python3.11 python3.11-devel

# Install PostgreSQL 14
sudo dnf install -y postgresql14-server postgresql14-contrib
sudo postgresql-14-setup initdb
sudo systemctl enable postgresql-14
sudo systemctl start postgresql-14

# Install Tesseract
sudo dnf install -y tesseract tesseract-langpack-eng

# Install Poppler
sudo dnf install -y poppler-utils

# Install Redis
sudo dnf install -y redis
sudo systemctl enable redis
sudo systemctl start redis

# Install build tools
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y postgresql-devel

# Clone and setup (same as Ubuntu)
git clone https://github.com/onefsmedia/ocr-agent-pro.git
cd ocr-agent-pro
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/setup/setup_database.py
python server.py
```

### Windows (Complete Installation)

```powershell
# Install Python 3.11
winget install Python.Python.3.11

# Install PostgreSQL
winget install PostgreSQL.PostgreSQL

# Install Tesseract
choco install tesseract
# Or download from: https://github.com/UB-Mannheim/tesseract/wiki

# Install Git
winget install Git.Git

# Clone repository
git clone https://github.com/onefsmedia/ocr-agent-pro.git
cd ocr-agent-pro

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install packages
pip install --upgrade pip
pip install -r requirements.txt

# Install pgvector extension for PostgreSQL
# Download from: https://github.com/pgvector/pgvector/releases
# Follow installation instructions

# Setup
copy .env.example .env
# Edit .env with your settings
python scripts\setup\setup_database.py
python server.py
```

### macOS (Complete Installation)

```bash
#!/bin/bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Install PostgreSQL with pgvector
brew install postgresql@14
brew install pgvector
brew services start postgresql@14

# Install Tesseract
brew install tesseract
brew install tesseract-lang

# Install Poppler
brew install poppler

# Install Redis
brew install redis
brew services start redis

# Clone repository
git clone https://github.com/onefsmedia/ocr-agent-pro.git
cd ocr-agent-pro

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install packages
pip install --upgrade pip
pip install -r requirements.txt

# Setup
cp .env.example .env
# Edit .env with your settings
python scripts/setup/setup_database.py
python server.py
```

---

## 🎯 GPU Setup (Optional)

### NVIDIA GPU Setup for CUDA

**1. Install NVIDIA Drivers:**

```bash
# Ubuntu/Debian
sudo apt install -y nvidia-driver-525

# Check installation
nvidia-smi
```

**2. Install CUDA Toolkit:**

```bash
# Ubuntu/Debian (CUDA 12.0)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install -y cuda-12-0

# Add to PATH
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

**3. Install PyTorch with CUDA:**

```bash
# Activate virtual environment first
source .venv/bin/activate

# Install PyTorch with CUDA 12.0
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu120
```

**4. Verify GPU Detection:**

```python
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
```

**5. Configure Application (.env):**

```bash
# Enable GPU for DeepSeek OCR
CUDA_VISIBLE_DEVICES=0
USE_GPU=true
```

### Docker with NVIDIA GPU

**Install NVIDIA Container Toolkit:**

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker
```

**Test GPU in Docker:**

```bash
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

---

## ✅ Post-Installation Verification

### 1. Check Python Version

```bash
python --version
# Should output: Python 3.11.x
```

### 2. Check PostgreSQL

```bash
psql --version
# Should output: psql (PostgreSQL) 14.x or higher

# Test connection
psql -U postgres -c "SELECT version();"
```

### 3. Check pgvector Extension

```bash
psql -U postgres -d ocr_agent -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### 4. Check Tesseract

```bash
tesseract --version
# Should output: tesseract 4.x or 5.x

# Test OCR
tesseract --list-langs
```

### 5. Check Redis

```bash
redis-cli ping
# Should output: PONG
```

### 6. Check Python Packages

```bash
pip list | grep -E "Flask|psycopg2|sentence-transformers|openai"
```

### 7. Check Application Health

```bash
# Start server
python server.py

# In another terminal, check health endpoint
curl http://localhost:5000/api/health
```

### 8. Verify GPU (if installed)

```bash
nvidia-smi
# Should show GPU utilization

python -c "import torch; print(torch.cuda.is_available())"
# Should output: True
```

---

## 📊 Resource Requirements Summary

| Component | Minimum | Recommended | Enterprise |
|-----------|---------|-------------|------------|
| **CPU** | 4 cores | 8 cores | 16+ cores |
| **RAM** | 8GB | 16GB | 32GB+ |
| **Storage** | 50GB | 200GB SSD | 1TB+ NVMe |
| **GPU VRAM** | - (optional) | 12GB | 24GB+ |
| **Network** | 100 Mbps | 1 Gbps | 10 Gbps |

---

## 🔍 Troubleshooting

### Common Issues

**1. Python package installation fails:**
```bash
# Install build tools
sudo apt install build-essential python3-dev  # Ubuntu
pip install --upgrade pip setuptools wheel
```

**2. PostgreSQL connection fails:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql
# Check port
sudo netstat -tulpn | grep 5432
```

**3. Tesseract not found:**
```bash
# Ubuntu: Check installation
which tesseract
# Add to PATH if needed
export PATH=/usr/bin:$PATH
```

**4. GPU not detected:**
```bash
# Check NVIDIA driver
nvidia-smi
# Reinstall CUDA toolkit if needed
```

**5. Out of memory errors:**
```bash
# Increase swap space (Linux)
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 📞 Support

For installation issues:
- Check: [docs/troubleshooting/](docs/troubleshooting/)
- GitHub Issues: https://github.com/onefsmedia/ocr-agent-pro/issues
- Documentation: [DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md)

---

## ☁️ Cloud Deployment Options

OCR Agent Pro can be deployed on various cloud platforms for scalable, managed infrastructure.

### AWS (Amazon Web Services)

#### Recommended Services:

**Compute:**
- **Amazon EC2** - Virtual machines for application hosting
  - Instance Types: 
    - Development: `t3.large` (2 vCPU, 8GB RAM) - $0.0832/hour
    - Production: `c5.2xlarge` (8 vCPU, 16GB RAM) - $0.34/hour
    - GPU: `g5.xlarge` (4 vCPU, 16GB RAM, 24GB GPU) - $1.006/hour
  - OS: Ubuntu 22.04 LTS AMI
  - Storage: 200GB gp3 SSD

- **Amazon ECS/EKS** - Containerized deployment
  - Use Fargate for serverless containers
  - Or EC2 instances for more control

**Database:**
- **Amazon RDS for PostgreSQL**
  - Version: PostgreSQL 14 or 16
  - Instance: `db.r6g.large` (2 vCPU, 16GB RAM) - $0.252/hour
  - Storage: 200GB gp3 SSD
  - **Note:** pgvector extension available on RDS PostgreSQL 15.2+
  - Enable automated backups
  - Multi-AZ for high availability

**Storage:**
- **Amazon S3** - Document storage
  - Standard tier for active documents
  - Intelligent-Tiering for automatic cost optimization
  - Lifecycle policies for archival
  - Estimated: $0.023/GB/month

- **Amazon EFS** - Shared file system
  - For uploads and temporary processing
  - Automatic scaling

**Caching:**
- **Amazon ElastiCache for Redis**
  - Instance: `cache.r6g.large` (2 vCPU, 13.07GB RAM) - $0.201/hour
  - Cluster mode for high availability

**Load Balancing:**
- **Application Load Balancer (ALB)**
  - SSL/TLS termination
  - Health checks
  - Auto-scaling support
  - Cost: $0.0225/hour + $0.008/LCU-hour

**AI Services (Optional Alternatives):**
- **Amazon Textract** - OCR service (alternative to Tesseract)
- **Amazon Bedrock** - Managed LLM (alternative to Ollama)
- **Amazon OpenSearch** - Vector search (alternative to pgvector)

#### AWS Deployment Architecture:

```
┌─────────────────────────────────────────────────────────┐
│ Route 53 (DNS)                                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ CloudFront (CDN)                                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ Application Load Balancer (ALB)                         │
└────────┬──────────────────────────────┬─────────────────┘
         │                              │
┌────────▼─────────┐         ┌──────────▼──────────┐
│ EC2 Auto Scaling │         │ EC2 Auto Scaling    │
│ (App Instances)  │         │ (App Instances)     │
│ - Ubuntu 22.04   │         │ - Ubuntu 22.04      │
│ - Docker         │         │ - Docker            │
│ - OCR Agent Pro  │         │ - OCR Agent Pro     │
└────────┬─────────┘         └──────────┬──────────┘
         │                              │
         ├──────────────┬───────────────┤
         │              │               │
┌────────▼─────┐ ┌──────▼──────┐ ┌─────▼──────┐
│ RDS          │ │ ElastiCache │ │ S3 Bucket  │
│ PostgreSQL   │ │ Redis       │ │ Documents  │
│ (pgvector)   │ │             │ │            │
└──────────────┘ └─────────────┘ └────────────┘
```

#### AWS Deployment Steps:

```bash
# 1. Create EC2 instance
aws ec2 run-instances \
  --image-id ami-0c7217cdde317cfec \  # Ubuntu 22.04
  --instance-type c5.2xlarge \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx

# 2. Connect via SSH
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# 3. Install dependencies (same as Ubuntu installation above)
# 4. Configure .env with RDS and ElastiCache endpoints
# 5. Deploy application
```

#### AWS Cost Estimate (Monthly):

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| EC2 (c5.2xlarge) | 2 instances, 24/7 | ~$490 |
| RDS PostgreSQL | db.r6g.large | ~$184 |
| ElastiCache Redis | cache.r6g.large | ~$147 |
| S3 Storage | 500GB | ~$12 |
| ALB | Standard | ~$25 |
| Data Transfer | 100GB out | ~$9 |
| **Total** | | **~$867/month** |

---

### Azure (Microsoft Azure)

#### Recommended Services:

**Compute:**
- **Azure Virtual Machines**
  - Series: D-series (general purpose) or F-series (compute optimized)
  - Size: `Standard_D4s_v5` (4 vCPU, 16GB RAM) - $0.192/hour
  - GPU: `NC6s_v3` (6 vCPU, 112GB RAM, Tesla V100) - $3.06/hour
  - OS: Ubuntu 22.04 LTS

- **Azure Container Instances (ACI)** or **Azure Kubernetes Service (AKS)**
  - Containerized deployment
  - Auto-scaling support

**Database:**
- **Azure Database for PostgreSQL - Flexible Server**
  - Version: PostgreSQL 14 or 16
  - Tier: General Purpose
  - Compute: `Standard_D4s_v3` (4 vCPU, 16GB RAM) - $0.272/hour
  - Storage: 256GB Premium SSD
  - pgvector extension supported
  - Automated backups
  - High availability option

**Storage:**
- **Azure Blob Storage** - Document storage
  - Hot tier for active documents
  - Cool/Archive tiers for older documents
  - Cost: ~$0.018/GB/month (hot tier)

- **Azure Files** - Shared file system
  - Premium tier for better performance

**Caching:**
- **Azure Cache for Redis**
  - Tier: Standard
  - Size: C3 (6GB cache) - $0.336/hour
  - High availability with zone redundancy

**Load Balancing:**
- **Azure Application Gateway** or **Azure Load Balancer**
  - SSL/TLS termination
  - WAF capabilities
  - Health probes

**AI Services (Optional Alternatives):**
- **Azure Computer Vision** - OCR service
- **Azure OpenAI Service** - GPT models
- **Azure Cognitive Search** - Vector search

#### Azure Deployment Steps:

```bash
# 1. Create resource group
az group create --name ocr-agent-rg --location eastus

# 2. Create VM
az vm create \
  --resource-group ocr-agent-rg \
  --name ocr-agent-vm \
  --image Ubuntu2204 \
  --size Standard_D4s_v5 \
  --admin-username azureuser \
  --generate-ssh-keys

# 3. Create PostgreSQL server
az postgres flexible-server create \
  --resource-group ocr-agent-rg \
  --name ocr-agent-db \
  --location eastus \
  --admin-user dbadmin \
  --admin-password <secure-password> \
  --sku-name Standard_D4s_v3 \
  --version 14 \
  --storage-size 256

# 4. Enable pgvector extension
az postgres flexible-server parameter set \
  --resource-group ocr-agent-rg \
  --server-name ocr-agent-db \
  --name azure.extensions \
  --value VECTOR

# 5. SSH to VM and deploy application
```

#### Azure Cost Estimate (Monthly):

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| VM (Standard_D4s_v5) | 1 instance, 24/7 | ~$140 |
| PostgreSQL Flexible | Standard_D4s_v3 | ~$198 |
| Redis Cache | Standard C3 | ~$245 |
| Blob Storage | 500GB hot tier | ~$9 |
| Load Balancer | Standard | ~$20 |
| Bandwidth | 100GB out | ~$8 |
| **Total** | | **~$620/month** |

---

### Google Cloud Platform (GCP)

#### Recommended Services:

**Compute:**
- **Google Compute Engine (GCE)**
  - Machine Type: `n2-standard-4` (4 vCPU, 16GB RAM) - $0.194/hour
  - GPU: `n1-standard-4` + NVIDIA T4 - $0.35/hour + $0.35/hour GPU
  - OS: Ubuntu 22.04 LTS
  - Boot disk: 200GB SSD

- **Google Kubernetes Engine (GKE)**
  - Managed Kubernetes for containers
  - Auto-scaling and self-healing

**Database:**
- **Cloud SQL for PostgreSQL**
  - Version: PostgreSQL 14 or 15
  - Machine: `db-custom-4-16384` (4 vCPU, 16GB RAM) - $0.318/hour
  - Storage: 256GB SSD
  - pgvector extension supported
  - Automated backups
  - High availability configuration

**Storage:**
- **Google Cloud Storage** - Document storage
  - Standard storage class
  - Nearline/Coldline for archival
  - Cost: $0.020/GB/month

- **Filestore** - Managed NFS file system
  - For shared file access

**Caching:**
- **Cloud Memorystore for Redis**
  - Tier: Standard (high availability)
  - Memory: 6GB - $0.137/hour
  - Automatic failover

**Load Balancing:**
- **Cloud Load Balancing**
  - HTTPS load balancer
  - SSL/TLS termination
  - Global load balancing
  - DDoS protection

**AI Services (Optional Alternatives):**
- **Cloud Vision API** - OCR service
- **Vertex AI** - LLM and ML models
- **Vertex AI Vector Search** - Managed vector search

#### GCP Deployment Steps:

```bash
# 1. Create Compute Engine instance
gcloud compute instances create ocr-agent-vm \
  --machine-type=n2-standard-4 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=200GB \
  --boot-disk-type=pd-ssd \
  --zone=us-central1-a

# 2. Create Cloud SQL instance
gcloud sql instances create ocr-agent-db \
  --database-version=POSTGRES_14 \
  --tier=db-custom-4-16384 \
  --region=us-central1

# 3. Enable pgvector
gcloud sql instances patch ocr-agent-db \
  --database-flags=cloudsql.enable_pgvector=on

# 4. Create Cloud Storage bucket
gsutil mb -l us-central1 gs://ocr-agent-documents/

# 5. SSH to instance and deploy
gcloud compute ssh ocr-agent-vm --zone=us-central1-a
```

#### GCP Cost Estimate (Monthly):

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Compute Engine | n2-standard-4, 24/7 | ~$141 |
| Cloud SQL | db-custom-4-16384 | ~$232 |
| Memorystore Redis | 6GB standard | ~$100 |
| Cloud Storage | 500GB standard | ~$10 |
| Load Balancing | Standard | ~$18 |
| Network Egress | 100GB | ~$12 |
| **Total** | | **~$513/month** |

---

### DigitalOcean (Budget-Friendly Option)

#### Recommended Services:

**Compute:**
- **Droplets** (Virtual Machines)
  - Size: `s-4vcpu-8gb-amd` (4 vCPU, 8GB RAM, 160GB SSD) - $48/month
  - Size: `g-4vcpu-16gb` (4 vCPU, 16GB RAM, 100GB SSD) - $84/month
  - GPU Droplets: `gpu-h100x1-80gb` - Starting at $3.57/hour
  - OS: Ubuntu 22.04 LTS

**Database:**
- **Managed Database - PostgreSQL**
  - Plan: `db-s-4vcpu-8gb` (4 vCPU, 8GB RAM, 115GB disk) - $120/month
  - Version: PostgreSQL 14 or 15
  - Automated backups
  - **Note:** Check pgvector extension availability

**Storage:**
- **Spaces Object Storage** - S3-compatible storage
  - 250GB storage + 1TB transfer - $5/month
  - Additional storage: $0.02/GB/month

**Caching:**
- **Managed Redis**
  - Plan: `db-s-1vcpu-2gb` - $30/month
  - Or use self-hosted Redis on Droplet

**Load Balancing:**
- **DigitalOcean Load Balancer**
  - $12/month + $0.01/GB bandwidth

#### DigitalOcean Deployment Steps:

```bash
# 1. Create Droplet via CLI
doctl compute droplet create ocr-agent \
  --size s-4vcpu-8gb-amd \
  --image ubuntu-22-04-x64 \
  --region nyc3 \
  --ssh-keys <your-ssh-key-id>

# 2. Create Managed Database
doctl databases create ocr-agent-db \
  --engine pg \
  --version 14 \
  --size db-s-4vcpu-8gb \
  --region nyc3

# 3. Create Spaces bucket
doctl compute space create ocr-agent-docs --region nyc3

# 4. SSH to Droplet and deploy
ssh root@<droplet-ip>
```

#### DigitalOcean Cost Estimate (Monthly):

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Droplet | s-4vcpu-8gb-amd | $48 |
| Managed PostgreSQL | db-s-4vcpu-8gb | $120 |
| Managed Redis | db-s-1vcpu-2gb | $30 |
| Spaces Storage | 250GB + 1TB transfer | $5 |
| Load Balancer | Standard | $12 |
| **Total** | | **$215/month** |

---

### Linode (Akamai)

#### Recommended Services:

**Compute:**
- **Linode Instances**
  - Dedicated 8GB: 4 vCPU, 8GB RAM, 160GB SSD - $36/month
  - Dedicated 16GB: 8 vCPU, 16GB RAM, 320GB SSD - $72/month
  - GPU: RTX4000 (24GB VRAM) - $1.50/hour
  - OS: Ubuntu 22.04 LTS

**Database:**
- **Managed Database - PostgreSQL**
  - Plan: Dedicated 8GB (4 vCPU, 8GB RAM) - $70/month
  - Version: PostgreSQL 13, 14, or 15
  - Automated daily backups

**Storage:**
- **Object Storage** - S3-compatible
  - 250GB storage - $5/month
  - Flat-rate pricing: $5/month per 250GB

**Caching:**
- Self-hosted Redis on Linode instance

**Load Balancing:**
- **NodeBalancer**
  - $10/month per balancer
  - Includes 40Mbps bandwidth

#### Linode Cost Estimate (Monthly):

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Linode Instance | Dedicated 16GB | $72 |
| Managed PostgreSQL | Dedicated 8GB | $70 |
| Object Storage | 250GB | $5 |
| NodeBalancer | Standard | $10 |
| **Total** | | **$157/month** |

---

### Hetzner Cloud (Europe - Ultra Budget) 💰

**Location:** Germany (Nuremberg, Falkenstein, Helsinki, Ashburn VA)  
**Best For:** European deployments, budget-conscious projects, development/testing

#### Recommended Services:

**Compute:**
- **Cloud Servers (CX Line - Shared vCPU)**
  - CX21: 2 vCPU, 4GB RAM, 40GB SSD - €4.51/month (~$5/month)
  - CX31: 2 vCPU, 8GB RAM, 80GB SSD - €7.01/month (~$8/month)
  - CX41: 4 vCPU, 16GB RAM, 160GB SSD - €15.51/month (~$17/month)
  - CX51: 8 vCPU, 32GB RAM, 240GB SSD - €31.02/month (~$34/month)

- **Dedicated vCPU (CPX Line - Better Performance)**
  - CPX31: 4 vCPU, 8GB RAM, 160GB SSD - €12.60/month (~$14/month)
  - CPX41: 8 vCPU, 16GB RAM, 240GB SSD - €24.50/month (~$27/month)
  - CPX51: 16 vCPU, 32GB RAM, 360GB SSD - €47.00/month (~$52/month)

- **Dedicated Servers (AX Line - Bare Metal)**
  - AX41: AMD Ryzen 5 3600, 64GB RAM, 2x512GB NVMe - €46.41/month (~$51/month)
  - AX102: AMD Ryzen 9 7950X, 128GB RAM, 2x3.84TB NVMe - €129.73/month (~$143/month)

**Database:**
- Self-hosted PostgreSQL on Cloud Server
- Or use external managed database service

**Storage:**
- **Hetzner Storage Box** - Network storage (SFTP/CIFS/WebDAV)
  - 1TB - €3.81/month (~$4/month)
  - 5TB - €10.21/month (~$11/month)
  - 10TB - €19.61/month (~$22/month)
  - 20TB - €38.81/month (~$43/month)

**Volumes (Block Storage):**
- 10GB - €0.45/month per 10GB (~$0.50/month)
- 100GB - €4.80/month (~$5.30/month)

**Load Balancing:**
- **Load Balancer**
  - €5.39/month (~$6/month)
  - 20TB included traffic
  - Additional traffic: €1 per TB

**Networking:**
- 20TB included traffic per month
- Additional traffic: €1 per TB (~$1.10/TB)
- DDoS protection included (free)

#### Hetzner Deployment:

```bash
# Using Hetzner Cloud CLI (hcloud)
hcloud server create \
  --name ocr-agent \
  --type cx51 \
  --image ubuntu-22.04 \
  --location nbg1 \
  --ssh-key <your-key>

# Or use CPX line for dedicated vCPU
hcloud server create \
  --name ocr-agent-prod \
  --type cpx41 \
  --image ubuntu-22.04 \
  --location fsn1 \
  --ssh-key <your-key>
```

#### Hetzner Cost Estimates:

**Minimum Setup (Development):**
| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Cloud Server | CX31 (2 vCPU, 8GB) | ~$8 |
| Volume | 100GB block storage | ~$5 |
| **Total** | | **~$13/month** |

**Recommended Setup (Production):**
| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Cloud Server | CX51 (8 vCPU, 32GB) | ~$34 |
| Storage Box | 1TB | ~$4 |
| Load Balancer | Standard | ~$6 |
| **Total** | | **~$44/month** |

**High-Performance Setup:**
| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Dedicated Server | AX41 (Ryzen 5, 64GB, NVMe) | ~$51 |
| Storage Box | 5TB | ~$11 |
| **Total** | | **~$62/month** |

#### Key Features:

✅ **Exceptional Price-to-Performance** - Cheapest in Europe  
✅ **99.9% Uptime SLA**  
✅ **Free DDoS Protection** (up to 5 Gbps)  
✅ **20TB Free Traffic** per server per month  
✅ **Fast NVMe Storage** on all servers  
✅ **Hourly Billing** - Pay per second, billed hourly  
✅ **Snapshots & Backups** - €0.012/GB/month (~$0.013/GB)  
✅ **IPv4 & IPv6** included  
✅ **API & CLI Tools** for automation  

#### Important Notes:

⚠️ **Strict Acceptable Use Policy** - No spam, abuse, or illegal content  
⚠️ **German Data Protection Laws** - GDPR compliant  
⚠️ **No GPU Options** - Use Vast.ai or Paperspace for GPU  
⚠️ **Best for European Users** - Higher latency for Asia/Australia  
✅ **Excellent for:** Development, testing, small-to-medium production, European deployments

---

### Contabo (Global Budget Provider) 💰

**Location:** Germany, USA, UK, Singapore, Japan, Australia  
**Best For:** Maximum resources for minimum cost, budget hosting

#### VPS Plans (Virtual Private Servers):

**Cloud VPS:**
- **VPS S:** 4 vCPU, 6GB RAM, 100GB NVMe - €5.99/month (~$7/month)
- **VPS M:** 6 vCPU, 16GB RAM, 400GB NVMe - €11.99/month (~$13/month)
- **VPS L:** 8 vCPU, 30GB RAM, 800GB NVMe - €19.99/month (~$22/month)
- **VPS XL:** 10 vCPU, 60GB RAM, 1.6TB NVMe - €37.99/month (~$42/month)

**Storage VPS (Higher Storage):**
- **Storage VPS S:** 4 vCPU, 12GB RAM, 600GB SSD - €9.99/month (~$11/month)
- **Storage VPS M:** 6 vCPU, 24GB RAM, 1.2TB SSD - €17.99/month (~$20/month)
- **Storage VPS L:** 8 vCPU, 48GB RAM, 2.4TB SSD - €33.99/month (~$37/month)

**Dedicated Servers:**
- **AMD Ryzen 5 3600:** 6 cores, 64GB RAM, 1TB NVMe - €69.99/month (~$77/month)
- **AMD Ryzen 9 5950X:** 16 cores, 128GB RAM, 2TB NVMe - €139.99/month (~$154/month)

#### Key Features:

✅ **Incredible Storage** - 400GB-2.4TB included  
✅ **Unlimited Traffic** - No bandwidth limits  
✅ **32TB Snapshot Space** included  
✅ **DDoS Protection** included  
✅ **Global Locations** - 6 continents  
✅ **Free Backups** - Weekly snapshots  
✅ **99.95% Uptime SLA**  

#### Contabo Cost Estimate:

**Recommended Setup:**
| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Cloud VPS XL | 10 vCPU, 60GB RAM, 1.6TB | ~$42 |
| Object Storage | 500GB (if needed) | ~$3 |
| **Total** | | **~$45/month** |

#### Important Notes:

⚠️ **No Managed Database** - Self-host PostgreSQL  
⚠️ **Setup Fee** - €4.99-€9.99 one-time  
⚠️ **Minimum Contract** - 1 month  
⚠️ **Customer Support** - Basic (tickets only)  
✅ **Best for:** Maximum resources at minimum cost

---

### Vultr (Global, Developer-Friendly) 💰

**Location:** 25+ global locations (US, EU, Asia, Australia)  
**Best For:** Global reach, developer-friendly, good balance

#### Compute Plans:

**Regular Performance:**
- **1 vCPU, 1GB RAM, 25GB SSD** - $6/month
- **1 vCPU, 2GB RAM, 55GB SSD** - $12/month
- **2 vCPU, 4GB RAM, 80GB SSD** - $18/month
- **4 vCPU, 8GB RAM, 160GB SSD** - $36/month
- **6 vCPU, 16GB RAM, 320GB SSD** - $72/month
- **8 vCPU, 32GB RAM, 640GB SSD** - $144/month

**High-Performance (NVMe):**
- **1 vCPU, 2GB RAM, 32GB NVMe** - $10/month
- **2 vCPU, 4GB RAM, 64GB NVMe** - $20/month
- **4 vCPU, 8GB RAM, 128GB NVMe** - $40/month
- **8 vCPU, 16GB RAM, 256GB NVMe** - $80/month

**Cloud GPU (Optional):**
- **NVIDIA A100 (40GB):** 8 vCPU, 45GB RAM - $2.95/hour (~$2,124/month)
- **NVIDIA A16:** 4 vCPU, 16GB RAM - $0.50/hour (~$360/month)

**Managed Databases:**
- **PostgreSQL Starter:** 1 vCPU, 1GB RAM, 10GB - $15/month
- **PostgreSQL Business:** 2 vCPU, 4GB RAM, 55GB - $60/month
- **PostgreSQL Premium:** 4 vCPU, 8GB RAM, 115GB - $120/month

#### Key Features:

✅ **25+ Locations Worldwide** - Best global coverage  
✅ **Hourly Billing** - Pay per hour  
✅ **Free DDoS Protection**  
✅ **1-Click Apps** - WordPress, Docker, Kubernetes  
✅ **Managed Kubernetes** - $10/month per cluster  
✅ **Object Storage** - $5/month for 250GB  
✅ **Load Balancers** - $10/month  
✅ **Snapshots** - $0.05/GB/month  

#### Vultr Cost Estimate:

**Recommended Setup:**
| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Compute | 4 vCPU, 8GB RAM, 160GB | $36 |
| Managed PostgreSQL | 2 vCPU, 4GB RAM | $60 |
| Object Storage | 250GB | $5 |
| Load Balancer | Standard | $10 |
| **Total** | | **$111/month** |

**Budget Setup:**
| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| Compute | 4 vCPU, 8GB RAM, 160GB | $36 |
| Self-hosted DB | On same instance | $0 |
| **Total** | | **$36/month** |

---

### OVHcloud (European Giant) 💰

**Location:** France, UK, Germany, Poland, Canada, Australia, Singapore  
**Best For:** European deployments, French data protection

#### VPS Plans:

**Starter:**
- **1 vCore, 2GB RAM, 20GB SSD** - €3.50/month (~$4/month)
- **1 vCore, 2GB RAM, 40GB SSD** - €6.00/month (~$7/month)

**Value:**
- **2 vCore, 4GB RAM, 80GB SSD** - €12.00/month (~$13/month)
- **4 vCore, 8GB RAM, 160GB SSD** - €24.00/month (~$26/month)

**Essential:**
- **4 vCore, 8GB RAM, 160GB NVMe** - €33.00/month (~$36/month)
- **8 vCore, 16GB RAM, 320GB NVMe** - €66.00/month (~$73/month)

**Comfort:**
- **8 vCore, 32GB RAM, 640GB NVMe** - €132.00/month (~$145/month)

**Dedicated Servers (Bare Metal):**
- **Rise-1:** Intel Xeon E-2136, 32GB RAM, 2x500GB SSD - €59.99/month (~$66/month)
- **Advance-1:** AMD EPYC 7351P, 64GB RAM, 2x450GB NVMe - €89.99/month (~$99/month)

#### Managed Databases:

**PostgreSQL:**
- **Essential:** 2 vCore, 4GB RAM, 80GB - €36/month (~$40/month)
- **Business:** 4 vCore, 8GB RAM, 160GB - €72/month (~$79/month)

#### Key Features:

✅ **Anti-DDoS Protection** - Industry-leading  
✅ **99.95% SLA**  
✅ **Object Storage** - S3-compatible, €0.01/GB/month  
✅ **Load Balancer** - €10/month  
✅ **Kubernetes** - Managed K8s clusters  
✅ **GDPR Compliant** - European data laws  

#### OVHcloud Cost Estimate:

**Budget Setup:**
| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| VPS Value | 4 vCore, 8GB RAM, 160GB | ~$26 |
| Object Storage | 500GB | ~$5 |
| **Total** | | **~$31/month** |

---

### Scaleway (French Budget Cloud) 💰

**Location:** France (Paris, Amsterdam)  
**Best For:** European GDPR compliance, French hosting

#### Instance Plans:

**Development:**
- **DEV1-S:** 2 vCPU, 2GB RAM, 20GB SSD - €7.99/month (~$9/month)
- **DEV1-M:** 3 vCPU, 4GB RAM, 40GB SSD - €13.99/month (~$15/month)
- **DEV1-L:** 4 vCPU, 8GB RAM, 80GB SSD - €23.99/month (~$26/month)

**General Purpose (Production):**
- **GP1-XS:** 4 vCPU, 16GB RAM, 150GB NVMe - €23.99/month (~$26/month)
- **GP1-S:** 8 vCPU, 32GB RAM, 300GB NVMe - €47.99/month (~$53/month)
- **GP1-M:** 16 vCPU, 64GB RAM, 600GB NVMe - €95.99/month (~$106/month)

**Managed Databases:**
- **PostgreSQL DB-DEV-S:** 1 vCPU, 1GB RAM - €10/month (~$11/month)
- **PostgreSQL DB-GP-S:** 2 vCPU, 4GB RAM - €36/month (~$40/month)

**Object Storage:**
- Standard: €0.01/GB/month (~$0.011/GB)
- Glacier (Archive): €0.002/GB/month

#### Key Features:

✅ **100% Renewable Energy** - Eco-friendly  
✅ **Multi-AZ** - High availability  
✅ **DDoS Protection** included  
✅ **Kubernetes Kapsule** - Managed K8s  
✅ **Free Bandwidth** - 100Mbps unmetered  

#### Scaleway Cost Estimate:

**Recommended Setup:**
| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| GP1-XS | 4 vCPU, 16GB RAM, 150GB | ~$26 |
| Managed PostgreSQL | DB-GP-S | ~$40 |
| Object Storage | 500GB | ~$6 |
| **Total** | | **~$72/month** |

---

### Netcup (German Budget Host) 💰

**Location:** Germany (Nuremberg, Vienna)  
**Best For:** Absolute lowest prices, German quality

#### VPS Plans:

**VPS 200 G10s Plus:**
- 2 vCores, 2GB RAM, 40GB SSD - €2.99/month (~$3/month)

**VPS 500 G10s Plus:**
- 4 vCores, 4GB RAM, 80GB SSD - €5.49/month (~$6/month)

**VPS 1000 G10s Plus:**
- 6 vCores, 8GB RAM, 160GB SSD - €9.49/month (~$10/month)

**VPS 2000 G10s Plus:**
- 8 vCores, 16GB RAM, 320GB SSD - €17.99/month (~$20/month)

**VPS 4000 G10s Plus:**
- 10 vCores, 32GB RAM, 640GB SSD - €32.99/month (~$36/month)

**VPS 6000 G10s Plus:**
- 12 vCores, 48GB RAM, 960GB SSD - €47.99/month (~$53/month)

#### Key Features:

✅ **Extremely Low Prices** - Cheapest VPS in Europe  
✅ **100% Renewable Energy**  
✅ **DDoS Protection**  
✅ **Snapshots included**  
✅ **German Engineering**  

#### Netcup Cost Estimate:

**Ultra-Budget Setup:**
| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| VPS 2000 | 8 vCores, 16GB RAM, 320GB | ~$20 |
| **Total** | | **~$20/month** |

---

---

### Vast.ai (GPU-Optimized Budget Option) ⭐

**Best for:** AI workloads requiring GPUs at the lowest cost

#### Service Overview:

Vast.ai is a **decentralized GPU marketplace** offering consumer and datacenter GPUs at 3-5x lower prices than traditional cloud providers. Perfect for OCR Agent Pro's AI/LLM inference and DeepSeek OCR processing.

#### Available GPU Configurations:

**Consumer GPUs (Best Value):**
- **RTX 4090** - 24GB VRAM, 16,384 CUDA cores
  - On-demand: $0.34-0.56/hour (~$245-404/month)
  - Interruptible: $0.17-0.34/hour (~$122-245/month)
  
- **RTX 3090** - 24GB VRAM, 10,496 CUDA cores
  - On-demand: $0.24-0.42/hour (~$173-302/month)
  - Interruptible: $0.12-0.24/hour (~$86-173/month)
  
- **RTX 4080** - 16GB VRAM, 9,728 CUDA cores
  - On-demand: $0.29-0.48/hour (~$209-346/month)
  - Interruptible: $0.14-0.29/hour (~$101-209/month)

**Datacenter GPUs (Production):**
- **A100 (40GB)** - Professional ML workload
  - On-demand: $0.89-1.39/hour (~$641-1,001/month)
  - Interruptible: $0.45-0.89/hour (~$324-641/month)
  
- **A6000 (48GB)** - High VRAM for large models
  - On-demand: $0.59-0.99/hour (~$425-713/month)
  - Interruptible: $0.29-0.59/hour (~$209-425/month)

#### Instance Types:

**On-Demand:**
- Guaranteed availability until you stop
- Higher price but reliable
- Best for production workloads

**Interruptible (3-5x cheaper):**
- Can be reclaimed if someone bids higher
- Significantly lower cost
- Best for development/testing
- Automatic instance migration available

#### Key Features:

✅ **Ultra-Low GPU Pricing** - 70-80% cheaper than AWS/GCP  
✅ **Wide GPU Selection** - RTX 3060 to H100  
✅ **Flexible Billing** - Per-second billing, no commitments  
✅ **Pre-configured Docker** - PyTorch, TensorFlow ready  
✅ **SSH Access** - Full root access  
✅ **Jupyter Notebook** - Built-in for ML workflows  
✅ **Storage** - Persistent storage options available  

#### Deployment Steps:

```bash
# 1. Create account at https://vast.ai
# 2. Add payment method (credit card or crypto)
# 3. Search for instance with filters:
#    - GPU: RTX 4090 or RTX 3090
#    - RAM: 32GB+
#    - Storage: 200GB+
#    - DLPerf: >50 (performance score)

# 4. Select instance and click "Rent"
# 5. Choose template: "PyTorch" or "TensorFlow"
# 6. SSH into instance
ssh -p <port> root@<host>.vast.ai -L 5000:localhost:5000

# 7. Install OCR Agent Pro
git clone https://github.com/onefsmedia/ocr-agent-pro.git
cd ocr-agent-pro
pip install -r requirements.txt

# 8. Configure .env with Vast.ai specifics
# 9. Run application
python app.py
```

#### Vast.ai Configuration (.env):

```bash
# GPU-optimized settings for Vast.ai
CUDA_VISIBLE_DEVICES=0
USE_GPU=true
GPU_ACCELERATION=true

# LLM with GPU
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b  # or deepseek-coder

# OCR with GPU (if using DeepSeek)
DEEPSEEK_OCR_ENABLED=true
DEEPSEEK_OCR_USE_GPU=true

# Performance settings
TORCH_CUDA_ARCH_LIST="8.9"  # For RTX 4090
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

#### Vast.ai Cost Comparison:

| GPU Model | Vast.ai (Interruptible) | AWS (On-Demand) | Savings |
|-----------|-------------------------|-----------------|---------|
| RTX 4090 | $0.17-0.34/hour | ~$1.50/hour | 78-88% |
| RTX 3090 | $0.12-0.24/hour | ~$1.20/hour | 80-90% |
| A100 (40GB) | $0.45-0.89/hour | $3.06/hour | 71-85% |
| A6000 | $0.29-0.59/hour | $2.45/hour | 76-88% |

#### Recommended Vast.ai Setup:

**For Production:**
- GPU: RTX 4090 (24GB) - On-demand
- RAM: 64GB
- Storage: 500GB NVMe
- Cost: ~$350-450/month
- External PostgreSQL (DigitalOcean/Linode managed DB)

**For Development:**
- GPU: RTX 3090 (24GB) - Interruptible
- RAM: 32GB
- Storage: 200GB SSD
- Cost: ~$120-180/month
- Self-hosted PostgreSQL on same instance

#### Important Notes:

⚠️ **Not for database hosting** - Use external managed database (DigitalOcean, Linode, or Supabase)  
⚠️ **Interruptible instances** - May be reclaimed (save work frequently)  
⚠️ **Variable pricing** - Prices fluctuate based on supply/demand  
⚠️ **Network speeds vary** - Check bandwidth before committing  
✅ **Best for GPU-heavy workloads** - DeepSeek OCR, LLM inference, embeddings  

---

### Paperspace (AI/ML Platform) ⭐

**Best for:** Managed ML infrastructure with Jupyter notebooks and GPU instances

#### Service Overview:

Paperspace (by Digital Ocean) offers managed GPU instances specifically designed for AI/ML workloads with seamless integration for ML frameworks.

#### Gradient (Managed ML Platform):

**Free Tier:**
- 1x CPU instance (M4000)
- 5GB storage
- Perfect for testing and development
- **Free forever** with limitations

**Growth Plan - $8/month:**
- Access to better GPUs
- 200GB storage included
- Team collaboration tools
- Priority support

**Pro Plan - $39/month:**
- Access to all GPU types
- 1TB storage
- Advanced autoscaling
- Dedicated support

#### GPU Instance Pricing (Gradient):

**Entry-Level GPUs:**
- **RTX 4000 (8GB)** - $0.51/hour (~$367/month)
  - Good for: Development, small models
  
- **RTX 5000 (16GB)** - $0.78/hour (~$562/month)
  - Good for: Production, medium models

**High-Performance GPUs:**
- **A4000 (16GB)** - $0.76/hour (~$547/month)
  - Good for: Production workloads
  
- **A5000 (24GB)** - $1.38/hour (~$994/month)
  - Good for: Large models, high throughput
  
- **A6000 (48GB)** - $2.07/hour (~$1,490/month)
  - Good for: Very large models, multi-model serving

- **A100 (40GB)** - $3.09/hour (~$2,225/month)
  - Good for: Enterprise AI workloads

**Multi-GPU Options:**
- **4x A100 (40GB)** - $12.00/hour (~$8,640/month)
- **8x A100 (80GB)** - $32.77/hour (~$23,595/month)

#### Core Compute (Virtual Machines):

**CPU Instances:**
- **C4 - Starter:** 4 cores, 8GB RAM, 50GB SSD - $0.09/hour (~$65/month)
- **C5 - Standard:** 8 cores, 30GB RAM, 50GB SSD - $0.28/hour (~$202/month)
- **C7 - Performance:** 12 cores, 60GB RAM, 50GB SSD - $0.56/hour (~$403/month)

**GPU Instances:**
- **P4000 (8GB):** 8 cores, 30GB RAM, 250GB SSD - $0.51/hour (~$367/month)
- **P5000 (16GB):** 8 cores, 30GB RAM, 250GB SSD - $0.78/hour (~$562/month)
- **P6000 (24GB):** 8 cores, 30GB RAM, 250GB SSD - $1.10/hour (~$792/month)
- **V100 (16GB):** 8 cores, 30GB RAM, 250GB SSD - $2.30/hour (~$1,656/month)
- **A4000 (16GB):** 8 cores, 45GB RAM, 512GB SSD - $0.76/hour (~$547/month)
- **A6000 (48GB):** 8 cores, 45GB RAM, 512GB SSD - $2.07/hour (~$1,490/month)

#### Key Features:

✅ **Jupyter Notebooks** - Built-in web IDE  
✅ **Pre-configured Environments** - PyTorch, TensorFlow, FastAPI ready  
✅ **Persistent Storage** - Data survives instance stops  
✅ **One-Click Deployments** - Deploy models as APIs  
✅ **Team Collaboration** - Share notebooks and datasets  
✅ **Autoscaling** - Automatic resource scaling  
✅ **Metrics & Monitoring** - Built-in performance tracking  
✅ **Integrated GitHub** - Direct repo cloning  

#### Deployment Options:

**1. Gradient Notebooks (Recommended for Dev):**
```bash
# Create notebook via web UI at console.paperspace.com
# Choose template: PyTorch + GPU
# Clone repository in notebook:
!git clone https://github.com/onefsmedia/ocr-agent-pro.git
%cd ocr-agent-pro
!pip install -r requirements.txt

# Run application
!python app.py
```

**2. Gradient Deployments (Recommended for Production):**
```yaml
# deployment.yaml
image: paperspace/fastapi:latest
port: 5000
resources:
  replicas: 2
  instanceType: A4000
env:
  - name: DATABASE_URL
    value: postgresql://user:pass@host:5432/db
  - name: FLASK_ENV
    value: production
```

**3. Core Compute VMs (Full Control):**
```bash
# 1. Create machine via web UI or CLI
paperspace machines create \
  --machineType P5000 \
  --size 250 \
  --billingType hourly \
  --machineName ocr-agent \
  --templateId t7m0y9x

# 2. SSH into machine
paperspace machines ssh <machine-id>

# 3. Install OCR Agent Pro
git clone https://github.com/onefsmedia/ocr-agent-pro.git
cd ocr-agent-pro
pip install -r requirements.txt

# 4. Configure and run
python app.py
```

#### Paperspace Configuration (.env):

```bash
# GPU settings
CUDA_VISIBLE_DEVICES=0
USE_GPU=true
GPU_ACCELERATION=true

# Use Paperspace S3-compatible storage
PAPERSPACE_API_KEY=your-api-key
STORAGE_BACKEND=paperspace

# Or use external database
DATABASE_URL=postgresql://user:pass@external-db:5432/ocr_agent

# LLM configuration
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b
```

#### Paperspace Cost Estimates:

**Development Setup:**
- Instance: P4000 (8GB GPU) - $367/month
- Storage: 250GB included
- PostgreSQL: Self-hosted on same instance
- **Total: ~$367/month**

**Production Setup:**
- Instance: A4000 (16GB GPU) - $547/month
- Storage: 512GB included
- External DB: DigitalOcean managed PostgreSQL - $120/month
- **Total: ~$667/month**

**High-Performance Setup:**
- Instance: A5000 (24GB GPU) - $994/month
- Storage: 1TB
- External DB: DigitalOcean managed PostgreSQL - $120/month
- Redis: Managed - $30/month
- **Total: ~$1,144/month**

#### Paperspace vs Other Providers:

| Feature | Paperspace | AWS | Vast.ai |
|---------|-----------|-----|---------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **GPU Pricing** | Medium | High | Very Low |
| **ML Tools** | Excellent | Good | Basic |
| **Reliability** | High | Very High | Variable |
| **Support** | Good | Enterprise | Community |

#### When to Choose Paperspace:

✅ **Need Jupyter notebooks** for development  
✅ **ML-focused workflow** with pre-configured environments  
✅ **Team collaboration** on AI projects  
✅ **Managed deployments** without DevOps complexity  
✅ **Don't want to manage infrastructure**  

❌ **Avoid if:** Need lowest possible GPU cost (use Vast.ai)  
❌ **Avoid if:** Need enterprise SLAs (use AWS/Azure/GCP)  
❌ **Avoid if:** Need complex networking/VPC setup  

#### Paperspace + External Services (Best Combo):

```bash
# Paperspace for GPU compute + DeepSeek OCR
GPU_PROVIDER=paperspace
PAPERSPACE_INSTANCE=A4000

# DigitalOcean for managed database
DATABASE_URL=postgresql://user:pass@do-db.db.ondigitalocean.com:25060/ocr_agent

# DigitalOcean for Redis cache
REDIS_URL=redis://do-redis:25061

# DigitalOcean Spaces for document storage
UPLOAD_FOLDER=s3://ocr-documents
AWS_S3_ENDPOINT=https://nyc3.digitaloceanspaces.com
```

**Combined Cost:**
- Paperspace A4000: $547/month
- DigitalOcean PostgreSQL: $120/month  
- DigitalOcean Redis: $30/month
- DigitalOcean Spaces (500GB): $5/month
- **Total: ~$702/month**

---

---

### Cloud Deployment Comparison

#### Full-Featured Providers:

| Provider | Compute | Database | GPU Options | Monthly Cost | Best For |
|----------|---------|----------|-------------|--------------|----------|
| **AWS** | EC2 | RDS PostgreSQL | ✅ V100, A100, T4 | ~$867 | Enterprise, full ecosystem |
| **Azure** | VM | PostgreSQL Flexible | ✅ V100, A100, T4 | ~$620 | Microsoft integration |
| **GCP** | Compute Engine | Cloud SQL | ✅ T4, V100, A100 | ~$513 | AI/ML features |
| **DigitalOcean** | Droplet | Managed DB | ❌ None | ~$215 | Simplicity, startups |
| **Linode** | Instance | Managed DB | ✅ RTX6000 Ada | ~$157 | Good value, reliability |
| **Vultr** | Compute | Managed DB | ✅ A100, A16 | ~$111 | Global reach, 25+ locations |
| **Scaleway** | Instance | Managed DB | ❌ None | ~$72 | European, eco-friendly |

#### GPU-Optimized Providers:

| Provider | GPU Type | VRAM | Monthly Cost | Best For |
|----------|----------|------|--------------|----------|
| **Vast.ai** ⭐ | RTX 3090/4090 | 24GB | ~$86-404 | **Cheapest GPUs**, interruptible |
| **Paperspace** ⭐ | A4000/A5000 | 16-24GB | ~$367-994 | ML platform, Jupyter, managed |

#### Ultra-Budget Providers (Europe):

| Provider | Location | Compute | GPU Support | Monthly Cost | Best For |
|----------|----------|---------|-------------|--------------|----------|
| **Netcup** 🏆 | Germany | 8 vCPU, 16GB, 320GB | ❌ None | **~$20** | **Absolute cheapest** |
| **OVHcloud** | France/EU | 4 vCPU, 8GB, 160GB | ❌ None | ~$26-31 | Anti-DDoS, GDPR |
| **Hetzner** 💰 | Germany | 8 vCPU, 32GB, 240GB | ❌ None | ~$34-44 | Best price/performance |
| **Contabo** 💰 | Global | 10 vCPU, 60GB, 1.6TB | ❌ None | ~$42-45 | **Maximum storage** |

#### Budget Comparison (Self-Hosted Database):

| Provider | vCPU | RAM | Storage | Traffic | GPU Support | Monthly Cost |
|----------|------|-----|---------|---------|-------------|--------------|
| **Netcup** 🏆 | 8 | 16GB | 320GB SSD | Unlimited | ❌ None | **$20** |
| **Hetzner CX51** | 8 | 32GB | 240GB NVMe | 20TB | ❌ None | **$34** |
| **Vultr** | 4 | 8GB | 160GB SSD | 3TB | ✅ A100, A16 | **$36** |
| **Contabo VPS XL** | 10 | 60GB | 1.6TB NVMe | Unlimited | ❌ None | **$42** |
| **OVHcloud** | 4 | 8GB | 160GB SSD | Unlimited | ❌ None | **$26** |
| **Scaleway** | 4 | 16GB | 150GB NVMe | Unmetered | ❌ None | **$26** |

#### GPU-Specific Comparison:

**Consumer GPUs (Best Value for AI/OCR):**

| Provider | GPU Model | VRAM | CUDA Cores | Tensor Cores | Hourly | Monthly (730h) | Best Use Case |
|----------|-----------|------|------------|--------------|--------|----------------|---------------|
| **Vast.ai** ⭐ | RTX 3090 | 24GB | 10,496 | 328 (Gen 3) | $0.12-0.24 | **$86-173** | Dev/Testing (Interruptible) |
| **Vast.ai** ⭐ | RTX 4090 | 24GB | 16,384 | 512 (Gen 4) | $0.17-0.34 | **$122-245** | Production (Budget) |
| **Vast.ai** | RTX 4080 | 16GB | 9,728 | 304 (Gen 4) | $0.14-0.29 | $101-209 | Mid-range performance |
| **Vast.ai** | RTX 3080 | 10GB | 8,704 | 272 (Gen 3) | $0.08-0.18 | $58-131 | Budget option |

**Datacenter GPUs (Enterprise/Production):**

| Provider | GPU Model | VRAM | CUDA Cores | Tensor Cores | Hourly | Monthly (730h) | Best Use Case |
|----------|-----------|------|------------|--------------|--------|----------------|---------------|
| **Vast.ai** ⭐ | A6000 | 48GB | 10,752 | 336 (Gen 3) | $0.29-0.59 | **$209-425** | Large models, high VRAM |
| **Vast.ai** | A100 (40GB) | 40GB | 6,912 | 432 (Gen 3) | $0.45-0.89 | $324-641 | ML training |
| **Vast.ai** | A5000 | 24GB | 8,192 | 256 (Gen 3) | $0.21-0.45 | $151-324 | Balanced performance |
| **Paperspace** | RTX 4000 | 8GB | 2,304 | 288 (Gen 2) | $0.51 | $367 | Entry-level managed |
| **Paperspace** | A4000 | 16GB | 6,144 | 192 (Gen 3) | $0.76 | $547 | Production managed |
| **Paperspace** | A5000 | 24GB | 8,192 | 256 (Gen 3) | $1.38 | $994 | High-performance managed |
| **Paperspace** | A6000 | 48GB | 10,752 | 336 (Gen 3) | $2.07 | $1,490 | Large model managed |
| **Paperspace** | A100 (40GB) | 40GB | 6,912 | 432 (Gen 3) | $3.09 | $2,225 | Enterprise managed |
| **GCP** | T4 | 16GB | 2,560 | 320 (Gen 2) | $0.35 | $255 | GCP ecosystem |
| **GCP** | V100 | 16GB | 5,120 | 640 (Gen 1) | $2.48 | $1,810 | Legacy ML |
| **AWS** | g5.xlarge (A10G) | 24GB | 9,216 | 288 (Gen 3) | $1.006 | $734 | AWS ecosystem |
| **AWS** | p3.2xlarge (V100) | 16GB | 5,120 | 640 (Gen 1) | $3.06 | $2,234 | Legacy AWS |
| **Azure** | NC6s_v3 (V100) | 16GB | 5,120 | 640 (Gen 1) | $3.06 | $2,234 | Azure ecosystem |
| **Vultr** | A100 (40GB) | 40GB | 6,912 | 432 (Gen 3) | $2.95 | $2,124 | Vultr global network |
| **Vultr** | A16 | 16GB | 2,560 | 128 (Gen 4) | $0.50 | $360 | Inference optimized |
| **Linode** | RTX 6000 Ada | 48GB | 18,176 | 568 (Gen 4) | $1.50 | $1,080 | Latest Ada architecture |

**GPU Performance Tiers (for OCR Agent Pro):**

| Tier | Recommended GPU | VRAM | Monthly Cost | DeepSeek OCR | LLM Inference | Embeddings |
|------|----------------|------|--------------|--------------|---------------|------------|
| **Budget** | RTX 3080 10GB | 10GB | $58-131 | ⚠️ Limited | ✅ Small models | ✅ Yes |
| **Optimal** ⭐ | RTX 3090/4090 | 24GB | $86-245 | ✅ Full support | ✅ Up to 13B | ✅ Batch |
| **Professional** | A5000/A6000 | 24-48GB | $151-425 | ✅✅ Excellent | ✅ Up to 70B | ✅✅ Fast batch |
| **Enterprise** | A100 40GB | 40GB | $324-641 | ✅✅ Maximum | ✅ 70B+ models | ✅✅ Very fast |

**💡 Cost Savings:** 
- Vast.ai RTX 4090: **$245/month** vs AWS A10G: **$734/month** = **67% savings**
- Vast.ai A100: **$641/month** vs AWS p3.2xlarge: **$2,234/month** = **71% savings**
- Vast.ai offers 70-85% savings vs AWS/Azure/GCP for GPU workloads!

**🎯 OCR Agent Pro GPU Recommendations:**

| Workload | Recommended Setup | Monthly Cost | Performance |
|----------|------------------|--------------|-------------|
| **No GPU** | Tesseract OCR only, no LLM | $20-44 | Basic OCR |
| **Light GPU** | Vast.ai RTX 3090 + Hetzner DB | $109-196 | Good OCR + small LLM |
| **Optimal GPU** ⭐ | Vast.ai RTX 4090 + DO PostgreSQL | $260-380 | Excellent OCR + medium LLM |
| **Heavy GPU** | Vast.ai A6000 + DO PostgreSQL | $344-560 | Maximum OCR + large LLM |
| **Enterprise** | Paperspace A5000 managed | $1,144 | Fully managed with GPU |

---

### 💰 Ultra-Budget Deployment Guide

**Complete OCR Agent Pro deployment for under $50/month:**

#### Option 1: Single Server (Netcup - $20/month) 🏆

**What you get:**
- VPS 2000 G10s Plus: 8 vCPU, 16GB RAM, 320GB SSD
- All-in-one: App + PostgreSQL + Redis + OCR
- Perfect for: Small teams, development, testing

**Setup:**
```bash
# 1. Order VPS at netcup.de
# 2. SSH into server
ssh root@your-server-ip

# 3. Install everything
# (Use Ubuntu installation commands from earlier section)

# 4. Configure for single-server deployment
# All services on one machine
```

**Pros:**
- ✅ Absolute lowest cost ($20/month)
- ✅ Simple setup (one server)
- ✅ German quality & reliability

**Cons:**
- ⚠️ No automatic scaling
- ⚠️ Single point of failure
- ⚠️ Limited to Europe (higher latency elsewhere)

---

#### Option 2: Hetzner + External DB (DigitalOcean - $51/month)

**What you get:**
- Hetzner CX31: 2 vCPU, 8GB RAM, 80GB NVMe - $8/month (app server)
- DigitalOcean Managed PostgreSQL: 1GB RAM - $15/month
- Self-hosted Redis on Hetzner
- Hetzner Storage Box: 1TB - $4/month
- Hetzner Load Balancer (optional): $6/month

**Total:** $27-33/month (without LB) or $33-39/month (with LB)

**Setup:**
```bash
# 1. Create Hetzner VPS
hcloud server create --name ocr-app --type cx31 --image ubuntu-22.04

# 2. Create DigitalOcean managed database
doctl databases create ocr-db --engine pg --size db-s-1vcpu-1gb

# 3. Configure .env to use external database
DATABASE_URL=postgresql://user:pass@do-db.ondigitalocean.com:25060/ocr_agent
```

**Pros:**
- ✅ Managed database (backups, updates)
- ✅ Better reliability
- ✅ Room to scale

**Cons:**
- ⚠️ Slightly higher cost
- ⚠️ Multi-provider management

---

#### Option 3: Contabo Storage VPS (Single Server - $37/month)

**What you get:**
- Storage VPS L: 8 vCPU, 48GB RAM, 2.4TB SSD - $37/month
- All-in-one setup
- Massive storage for documents
- Unlimited traffic

**Best for:**
- Large document collections
- Document-heavy workflows
- Archive requirements

---

#### Option 4: Hetzner Dedicated (Best Performance - $51/month)

**What you get:**
- AX41 Dedicated Server: Ryzen 5 3600, 64GB RAM, 2x512GB NVMe - $51/month
- Bare metal performance
- No noisy neighbors
- Perfect for production

**Setup:**
```bash
# 1. Order at Hetzner Robot (https://robot.hetzner.com)
# 2. Install Ubuntu 22.04
# 3. Full installation (app + database + everything)
```

**Pros:**
- ✅ Bare metal performance
- ✅ 64GB RAM (plenty for everything)
- ✅ Dual NVMe in RAID
- ✅ Still under $60/month

---

### Budget Deployment Recommendation by Use Case:

#### Development & Testing:
**Winner: Netcup VPS 2000 ($20/month)**
- 8 vCPU, 16GB RAM, 320GB SSD
- All-in-one setup
- German location
- Perfect for learning and testing

#### Small Production (1-100 users):
**Winner: Hetzner CX51 ($34/month) + Storage Box ($4)**
- 8 vCPU, 32GB RAM, 240GB NVMe
- 1TB external storage
- 20TB traffic included
- Load balancer: +$6/month
- **Total: $38-44/month**

#### Medium Production (100-1000 users):
**Winner: Hetzner Dedicated AX41 ($51/month)**
- Bare metal: Ryzen 5 3600, 64GB RAM
- 2x512GB NVMe RAID
- Dedicated resources
- Add: DigitalOcean PostgreSQL replica (+$15)
- **Total: $66/month**

#### GPU Workloads (AI/OCR):
**Winner: Vast.ai RTX 3090 Interruptible ($86-173/month)**
- 24GB GPU for DeepSeek OCR & LLM
- + Hetzner CX31 for database ($8)
- + DigitalOcean managed PostgreSQL ($15)
- **Total: $109-196/month**

#### Global Deployment:
**Winner: Vultr (4 vCPU, 8GB - $36/month)**
- 25+ locations worldwide
- Low latency globally
- Managed PostgreSQL: +$60
- **Total: $96/month** (or $36 with self-hosted DB)

---

### Budget Optimization Tips:

1. **Self-Host Everything** - Run PostgreSQL, Redis, and app on same server
   - Saves: $50-100/month on managed services
   - Trade-off: More maintenance work

2. **Use European Providers** - Hetzner, Netcup, OVH, Contabo
   - Saves: 50-70% vs AWS/Azure
   - Trade-off: Europe-only or limited global locations

3. **Skip GPU Initially** - Use Tesseract OCR only (no DeepSeek)
   - Saves: $200-500/month
   - Trade-off: Lower OCR accuracy

4. **Use Object Storage Instead of Block Storage**
   - Hetzner Storage Box: $4/TB vs $50/TB for volumes
   - Saves: $40-100/month
   - Trade-off: SFTP/WebDAV instead of mounted filesystem

5. **Interruptible GPU Instances** (Vast.ai)
   - Saves: 50-70% on GPU costs
   - Trade-off: Can be reclaimed (use for dev/testing)

6. **Annual Billing** - Many providers offer discounts
   - Hetzner: No discount (already cheap)
   - Contabo: ~8% discount on annual
   - Vultr: No annual plans
   - Netcup: ~20% discount on annual

7. **Use Cloudflare** (Free Tier)
   - DDoS protection
   - CDN for static files
   - SSL certificates
   - Saves: $20-50/month

---

### Complete Budget Stack (Under $45/month):

```yaml
# Infrastructure
Compute: Hetzner CX51 (8 vCPU, 32GB RAM)      $34/month
Storage: Hetzner Storage Box (1TB)             $4/month  
CDN/DDoS: Cloudflare Free                      $0/month
DNS: Cloudflare Free                           $0/month
SSL: Let's Encrypt                             $0/month
Monitoring: UptimeRobot Free                   $0/month

# Software (All included)
PostgreSQL: Self-hosted on CX51                $0/month
Redis: Self-hosted on CX51                     $0/month
Tesseract OCR: Open source                     $0/month
Ollama (LLM): Self-hosted                      $0/month

# Optional Add-ons
Load Balancer: Hetzner LB                      $6/month
Backups: Hetzner Backup (20%)                  $7/month

TOTAL: $38-51/month (depending on options)
```

**What you can handle:**
- 500-1000 concurrent users
- 10,000+ documents
- 1TB document storage
- Full OCR + AI chatbot
- 99%+ uptime

---



#### For AWS:

```bash
# Database (RDS)
DATABASE_URL=postgresql://admin:password@ocr-db.xxxxx.us-east-1.rds.amazonaws.com:5432/ocr_agent

# Redis (ElastiCache)
REDIS_URL=redis://ocr-cache.xxxxx.use1.cache.amazonaws.com:6379

# Storage (S3)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=ocr-agent-documents
AWS_REGION=us-east-1
UPLOAD_FOLDER=s3://ocr-agent-documents/uploads
STORAGE_PATH=s3://ocr-agent-documents/storage

# Optional: Use AWS Bedrock for LLM
USE_AWS_BEDROCK=true
AWS_BEDROCK_MODEL=anthropic.claude-v2
```

#### For Azure:

```bash
# Database (Azure PostgreSQL)
DATABASE_URL=postgresql://dbadmin@ocr-db:password@ocr-db.postgres.database.azure.com:5432/ocr_agent?sslmode=require

# Redis (Azure Cache)
REDIS_URL=rediss://:password@ocr-cache.redis.cache.windows.net:6380

# Storage (Blob Storage)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_CONTAINER_NAME=documents
UPLOAD_FOLDER=azure://documents/uploads
STORAGE_PATH=azure://documents/storage

# Optional: Use Azure OpenAI
USE_AZURE_OPENAI=true
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key
```

#### For GCP:

```bash
# Database (Cloud SQL)
DATABASE_URL=postgresql://postgres:password@/ocr_agent?host=/cloudsql/project:region:instance

# Redis (Memorystore)
REDIS_URL=redis://10.0.0.3:6379

# Storage (Cloud Storage)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
GCS_BUCKET=ocr-agent-documents
UPLOAD_FOLDER=gs://ocr-agent-documents/uploads
STORAGE_PATH=gs://ocr-agent-documents/storage

# Optional: Use Vertex AI
USE_VERTEX_AI=true
VERTEX_AI_PROJECT=your-project-id
VERTEX_AI_LOCATION=us-central1
```

---

### Serverless Deployment Options

#### AWS Lambda + API Gateway

**Pros:**
- Pay per request (no idle costs)
- Auto-scaling
- No server management

**Cons:**
- 15-minute timeout limit
- Cold start latency
- Limited for long OCR processing

**Best For:** API endpoints, lightweight processing

#### Google Cloud Run

**Pros:**
- Container-based
- Auto-scaling to zero
- 60-minute timeout
- Pay per use

**Cons:**
- Request-based pricing
- May be expensive for sustained traffic

**Configuration:**
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/ocr-agent', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/ocr-agent']
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'ocr-agent'
      - '--image=gcr.io/$PROJECT_ID/ocr-agent'
      - '--platform=managed'
      - '--region=us-central1'
      - '--memory=4Gi'
      - '--cpu=2'
      - '--timeout=3600'
```

---

### Cloud Deployment Best Practices

#### Security:
1. **Use managed services** for database and caching
2. **Enable SSL/TLS** for all connections
3. **Use IAM roles** instead of access keys when possible
4. **Enable VPC** for network isolation
5. **Configure security groups/firewalls** properly
6. **Enable audit logging** (CloudTrail, Azure Monitor, Cloud Audit Logs)
7. **Use secrets management** (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)

#### Scalability:
1. **Use auto-scaling groups** for compute instances
2. **Configure database read replicas** for read-heavy workloads
3. **Implement caching** with Redis/Memcached
4. **Use CDN** (CloudFront, Azure CDN, Cloud CDN) for static assets
5. **Enable connection pooling** for database

#### Cost Optimization:
1. **Use reserved instances** for predictable workloads (30-70% savings)
2. **Use spot/preemptible instances** for fault-tolerant workloads (70-90% savings)
3. **Enable auto-scaling** to scale down during low traffic
4. **Use storage lifecycle policies** to archive old documents
5. **Monitor and set billing alerts**

#### Monitoring:
1. **CloudWatch** (AWS), **Azure Monitor** (Azure), **Cloud Monitoring** (GCP)
2. **Set up health checks** and uptime monitoring
3. **Configure log aggregation**
4. **Set up alerting** for errors and performance issues
5. **Use APM tools** (DataDog, New Relic, Application Insights)

---

## 📊 Cloud vs Self-Hosted Comparison

| Aspect | Cloud (AWS/Azure/GCP) | Self-Hosted (Own Servers) |
|--------|----------------------|---------------------------|
| **Initial Cost** | Low (pay-as-you-go) | High (hardware purchase) |
| **Monthly Cost** | $500-$1000+ | $50-200 (electricity, internet) |
| **Scalability** | Excellent (auto-scaling) | Limited (manual) |
| **Maintenance** | Managed by provider | Self-managed |
| **Availability** | 99.9%+ SLA | Depends on setup |
| **Security** | Enterprise-grade | Self-managed |
| **Best For** | Production, scaling | Development, small teams |

---

**Document Version:** 1.4  
**Last Updated:** November 3, 2025  
**Application Version:** OCR Agent Pro v1.3.0  

**Cloud Providers:** 13 comprehensive options with GPU specifications  
• **Enterprise:** AWS, Azure, GCP ($513-867/month) - V100, A100, T4 GPUs  
• **Mid-Range:** DigitalOcean, Linode, Vultr ($111-215/month) - Some with GPU  
• **Budget:** Hetzner, OVHcloud, Scaleway, Contabo ($26-45/month) - CPU only  
• **Ultra-Budget:** Netcup ($20/month) 🏆 - CPU only  
• **GPU-Optimized:** Vast.ai ($58-641/month), Paperspace ($367-2,225/month)  

**GPU Options:** 16 GPU models from RTX 3080 to A100  
**VRAM Range:** 8GB to 48GB  
**GPU Pricing:** From $58/month (Vast.ai RTX 3080) to $2,234/month (Azure V100)  
**Total Price Range:** From $20/month (Netcup VPS) to $8,640/month (AWS multi-GPU)
