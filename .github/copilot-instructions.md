# OCR Agent Project Instructions

This is a comprehensive OCR application with Flask, PostgreSQL with pgvector, OnlyOffice integrations, AI chatbot, and 6-panel dashboard for document processing and vector search.

## Project Setup Progress

- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements - OCR app with 6 panels, OnlyOffice integrations, AI chatbot
- [x] Scaffold the Project - Complete Flask application structure created
- [x] Customize the Project - Full OCR pipeline with AI integration implemented
- [x] Install Required Extensions - Dependencies defined in requirements.txt
- [x] Compile the Project - Ready for deployment with Docker/Podman
- [x] Create and Run Task - Multiple deployment options available
- [x] Launch the Project - Application ready to run
- [x] Ensure Documentation is Complete - Comprehensive docs provided

## Architecture Overview

Based on the n8n workflows analyzed, this OCR application will include:

1. **Document Ingestion Panel** - Upload and process PDFs with OCR
2. **Table View Panel** - Display processed documents and chunks
3. **Settings Panel** - Configure OnlyOffice sync, AI, database, API settings
4. **Database Status Panel** - Monitor PostgreSQL and pgvector status
5. **Chatbot Panel** - Interactive query interface with RAG
6. **Prompt Panel** - Configure system prompts for the chatbot

## Technology Stack

- **Backend**: Flask with SQLAlchemy and pgvector
- **OCR**: Tesseract + DeepSeek OCR (local processing)
- **AI**: Local LLM (Ollama/LM Studio) with RAG
- **Database**: PostgreSQL with pgvector extension
- **Frontend**: Flask templates with modern CSS/JS
- **Integrations**: OnlyOffice Document Server APIs
- **Deployment**: Docker/Podman containers