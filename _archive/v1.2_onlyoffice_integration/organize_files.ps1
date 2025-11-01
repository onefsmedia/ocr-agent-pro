# OCR Agent - File Organization Script
# Systematically moves files to organized structure

Write-Host "🔄 OCR Agent File Organization" -ForegroundColor Cyan
Write-Host "=" * 60

$ErrorActionPreference = 'SilentlyContinue'

# Move comprehensive test files to E2E
Write-Host "`n📦 Moving E2E tests..." -ForegroundColor Yellow
Move-Item "test_chatbot_comprehensive.py" "tests\e2e\" -Force
Move-Item "test_application.py" "tests\e2e\" -Force

# Move integration test files
Write-Host "📦 Moving integration tests..." -ForegroundColor Yellow
Move-Item "test_document_ingestion_final.py" "tests\integration\" -Force
Move-Item "test_onlyoffice_integration.py" "tests\integration\" -Force
Move-Item "test_api.py" "tests\integration\" -Force
Move-Item "test_500mb_processing.py" "tests\integration\" -Force

# Move unit test files
Write-Host "📦 Moving unit tests..." -ForegroundColor Yellow
Move-Item "test_llm_integration.py" "tests\unit\" -Force
Move-Item "test_pdf_ocr.py" "tests\unit\" -Force

# Archive old test files
Write-Host "📦 Archiving old test files..." -ForegroundColor Yellow
$oldTests = @(
    "test_document_ingestion.py",
    "test_onlyoffice.py",
    "test_enhanced_ingestion.py",
    "test_comprehensive_fixes.py",
    "test_chat_comprehensive.py",
    "test_enhanced_chatbot.py",
    "test_chatbot_direct.py",
    "test_chatbot_fix.py",
    "test_chatbot_manual.py",
    "test_chatbot_panel.py",
    "test_chatbot_ui.py",
    "test_chat_fix.py",
    "test_simple_chat.py",
    "test_scrollable_sessions.py"
)

foreach ($test in $oldTests) {
    if (Test-Path $test) {
        Move-Item $test "_archive\v1.1_server_fixes\" -Force
    }
}

# Move maintenance scripts
Write-Host "`n📦 Moving maintenance scripts..." -ForegroundColor Yellow
Move-Item "check_documents.py" "scripts\maintenance\" -Force
Move-Item "check-onlyoffice-status.py" "scripts\maintenance\" -Force
Move-Item "debug_chat.py" "scripts\maintenance\" -Force

# Move setup scripts
Write-Host "📦 Moving setup scripts..." -ForegroundColor Yellow
Move-Item "setup_database.py" "scripts\setup\" -Force
Move-Item "migrate_database.py" "scripts\setup\" -Force
Move-Item "setup_onlyoffice.py" "scripts\setup\" -Force
Move-Item "install_french_ocr.py" "scripts\setup\" -Force

# Move configuration scripts
Write-Host "📦 Moving configuration scripts..." -ForegroundColor Yellow
Move-Item "configure_onlyoffice.py" "scripts\configuration\" -Force
Move-Item "configure_large_files.py" "scripts\configuration\" -Force

# Move deployment scripts
Write-Host "📦 Moving deployment scripts..." -ForegroundColor Yellow
Move-Item "deploy-local.ps1" "scripts\deployment\" -Force
Move-Item "deploy-podman.ps1" "scripts\deployment\" -Force
Move-Item "podman-deploy.ps1" "scripts\deployment\" -Force
Move-Item "deploy-onlyoffice.ps1" "scripts\deployment\" -Force
Move-Item "deploy-onlyoffice-podman.ps1" "scripts\deployment\" -Force
Move-Item "install-postgresql.ps1" "scripts\deployment\" -Force
Move-Item "install-postgresql-native.ps1" "scripts\deployment\" -Force
Move-Item "start_server.ps1" "scripts\deployment\" -Force
Move-Item "start_waitress.ps1" "scripts\deployment\" -Force
Move-Item "verify_onlyoffice_8080.ps1" "scripts\maintenance\" -Force

# Move documentation
Write-Host "`n📦 Moving documentation..." -ForegroundColor Yellow
Move-Item "DEPLOYMENT_GUIDE.md" "docs\deployment\" -Force
Move-Item "DEPLOYMENT.md" "docs\deployment\" -Force
Move-Item "PODMAN_DEPLOYMENT.md" "docs\deployment\" -Force
Move-Item "WAITRESS_SETUP.md" "docs\deployment\" -Force
Move-Item "DATABASE_SETUP.md" "docs\deployment\" -Force

Move-Item "FEATURE_REVIEW.md" "docs\features\" -Force
Move-Item "CHATBOT_FIX_SUMMARY.md" "docs\features\" -Force
Move-Item "DOCUMENT_INGESTION_REPORT.md" "docs\features\" -Force
Move-Item "ENHANCED_CHAT_INTERFACE_COMPLETE.md" "docs\features\" -Force
Move-Item "ENHANCED_CONFIG_NAVIGATION_COMPLETE.md" "docs\features\" -Force
Move-Item "ENHANCED_PROMPT_LAYOUT_COMPLETE.md" "docs\features\" -Force
Move-Item "DEEPSEEK_INTEGRATION_COMPLETE.md" "docs\features\" -Force
Move-Item "500MB_PROCESSING_SUMMARY.md" "docs\features\" -Force

Move-Item "DOCKER_ISSUE_SUMMARY.md" "docs\troubleshooting\" -Force
Move-Item "PROBLEM_RESOLVED.md" "docs\troubleshooting\" -Force
Move-Item "ONLYOFFICE_PORT_8000_MANUAL_GUIDE.md" "docs\troubleshooting\" -Force

# Archive education-specific docs
Move-Item "BILINGUAL_EDUCATION_COMPLETE.md" "_archive\deprecated\" -Force
Move-Item "CAMEROON_EDUCATION_INTEGRATION.md" "_archive\deprecated\" -Force

# Archive remaining old files
Write-Host "`n📦 Archiving remaining old files..." -ForegroundColor Yellow
Move-Item "onlyoffice_solution.py" "_archive\v1.2_onlyoffice_integration\" -Force
Move-Item "config.py.backup" "_archive\deprecated\" -Force
Move-Item "waitress_config.json" "_archive\deprecated\" -Force

# Delete log files
Write-Host "`n🗑️  Removing old log files..." -ForegroundColor Yellow
Remove-Item "server_diagnostic.log" -Force
Remove-Item "onlyoffice-documentserver.exe" -Force

Write-Host "`n✅ File organization complete!" -ForegroundColor Green
Write-Host "`n📋 Summary:" -ForegroundColor Cyan
Write-Host "  • Tests organized into unit/integration/e2e"
Write-Host "  • Scripts organized by purpose"
Write-Host "  • Documentation organized by type"
Write-Host "  • Old files archived by version"
Write-Host "  • Deprecated files moved to _archive"
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Test application: python server.py"
Write-Host "  2. Run tests: pytest tests/"
Write-Host "  3. Review organized structure"
Write-Host "  4. Commit to Git"
