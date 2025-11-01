# GitHub Repository Setup Guide

Follow these steps to create a GitHub repository and push your OCR Agent Pro code.

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface (Recommended)

1. Go to **https://github.com/new**
2. Fill in repository details:
   - **Repository name**: `ocr-agent-pro` (or your preferred name)
   - **Description**: "OCR Agent Pro - AI-powered document processing with Flask, PostgreSQL, pgvector, and OnlyOffice integration"
   - **Visibility**: 
     - ✅ Public (if you want it public)
     - ✅ Private (if you want it private)
   - **❌ DO NOT** initialize with README (we have one already)
   - **❌ DO NOT** add .gitignore (we have one already)
   - **❌ DO NOT** choose a license yet (we'll add it later)

3. Click **"Create repository"**

4. You'll see a page with commands - **keep this page open**, we'll use those commands next!

### Option B: Using GitHub CLI (if you have `gh` installed)

```bash
gh repo create ocr-agent-pro --public --description "OCR Agent Pro - AI-powered document processing"
```

---

## Step 2: Initialize Git Repository Locally

Open PowerShell in your project directory and run:

```powershell
cd "C:\OCR Agent"

# Initialize Git repository
git init

# Add all files
git add .

# Check what will be committed (optional)
git status

# Create initial commit
git commit -m "feat: Initial commit - OCR Agent Pro v1.3.0

Complete OCR application with:
- 6-panel dashboard for document processing
- Flask backend with PostgreSQL + pgvector
- OnlyOffice Document Server integration
- AI chatbot with RAG (Ollama/OpenAI)
- Multi-format OCR (Tesseract + DeepSeek)
- Production-ready server (Waitress WSGI)
- Docker/Podman deployment support
- Comprehensive documentation

Features:
✅ Document ingestion (PDF, DOC, images)
✅ Vector semantic search
✅ AI-powered Q&A chatbot
✅ OnlyOffice document editing
✅ Large file processing (up to 500MB)
✅ Multi-language OCR support

Technical Stack:
- Python 3.11+
- Flask 3.0.0
- PostgreSQL 12+ with pgvector
- Tesseract OCR 4.0+
- Sentence Transformers
- LangChain + LLM integration

Project organized with:
- scripts/ - Utility scripts
- tests/ - Unit/Integration/E2E tests
- docs/ - Comprehensive documentation
- Clean root structure (11 files)

Version: 1.3.0 (Production Ready)
Date: November 2, 2025"
```

---

## Step 3: Connect to GitHub Repository

After creating the repository on GitHub, you'll see commands like this. Use them:

```powershell
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ocr-agent-pro.git

# Verify remote was added
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example with actual username:**
```powershell
# If your GitHub username is "johndoe"
git remote add origin https://github.com/johndoe/ocr-agent-pro.git
git push -u origin main
```

---

## Step 4: Verify Upload

1. Go to your GitHub repository page
2. You should see:
   - ✅ All your files and directories
   - ✅ README.md displayed on the main page
   - ✅ Complete file structure
   - ✅ Commit message visible

---

## Step 5: Add Repository Tags (Optional but Recommended)

```powershell
# Create version tag
git tag -a v1.3.0 -m "Version 1.3.0 - Production Ready

Major Features:
- Complete project reorganization
- Production-ready server
- Comprehensive documentation
- Full test suite
- Docker/Podman support"

# Push tags to GitHub
git push --tags
```

---

## Step 6: Update Repository Settings on GitHub

1. Go to your repository on GitHub
2. Click **"Settings"** tab
3. Configure:
   - **Description**: Add description and website URL
   - **Topics**: Add topics like: `ocr`, `flask`, `postgresql`, `ai`, `nlp`, `document-processing`, `python`, `onlyoffice`
   - **Social Preview**: Upload a preview image (optional)

---

## Step 7: Create GitHub Release (Optional)

1. Go to **"Releases"** tab on your repository
2. Click **"Create a new release"**
3. Choose tag: `v1.3.0`
4. Release title: `OCR Agent Pro v1.3.0 - Production Ready`
5. Description: Copy content from `CHANGELOG.md`
6. Attach files (optional): Installation scripts, documentation PDFs
7. Click **"Publish release"**

---

## Troubleshooting

### Error: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/ocr-agent-pro.git
```

### Error: "Permission denied"
You may need to authenticate:
1. **Using HTTPS**: GitHub will prompt for username/password or token
2. **Using SSH**: Set up SSH keys (see GitHub docs)
3. **Using GitHub CLI**: Run `gh auth login`

### Error: "failed to push some refs"
```powershell
# Pull first (if repository was initialized with README)
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Large files warning
If you get warnings about large files:
1. Check `.gitignore` is working
2. Remove large files: `git rm --cached <large-file>`
3. Consider using Git LFS for large files

---

## Important: Environment Variables

**⚠️ SECURITY WARNING**: Make sure `.env` file is NOT committed!

Check `.gitignore` includes:
```
.env
.env.local
.env.development
```

Verify:
```powershell
# This should show .env is ignored
git check-ignore .env

# This should NOT show .env in the list
git status
```

If `.env` was committed by mistake:
```powershell
git rm --cached .env
git commit -m "Remove .env from repository"
git push
```

---

## Post-Push Checklist

After pushing to GitHub, verify:

- [ ] All files visible on GitHub
- [ ] README.md renders correctly
- [ ] Documentation links work
- [ ] `.env` file is NOT visible (should be ignored)
- [ ] Project structure looks correct
- [ ] No sensitive data exposed (passwords, API keys)
- [ ] Commit history is clean
- [ ] Repository description added
- [ ] Topics/tags added

---

## Clone Instructions (For Others)

Add this to your README.md for others to clone:

```markdown
## Installation

\`\`\`bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ocr-agent-pro.git
cd ocr-agent-pro

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python scripts/setup/setup_database.py

# Start server
python server.py
\`\`\`
```

---

## Next Steps

1. **Set up GitHub Actions** (CI/CD):
   - Create `.github/workflows/tests.yml`
   - Automate testing on push/PR

2. **Enable GitHub Pages** (if needed):
   - For hosting documentation

3. **Add Collaborators**:
   - Settings → Collaborators

4. **Protect main branch**:
   - Settings → Branches → Add rule
   - Require pull request reviews

5. **Add issue templates**:
   - Create `.github/ISSUE_TEMPLATE/`

---

**Ready to push? Follow the steps above!** 🚀

**Your repository will be at**: `https://github.com/YOUR_USERNAME/ocr-agent-pro`
