# Tests Directory

Organized test suite for OCR Agent Pro.

## Directory Structure

### `/unit/`
Unit tests for individual components:
- `test_llm_integration.py` - LLM service tests
- `test_pdf_ocr.py` - OCR service tests

### `/integration/`
Integration tests for multi-component workflows:
- `test_document_ingestion_final.py` - Document upload and processing
- `test_onlyoffice_integration.py` - OnlyOffice integration
- `test_api.py` - API endpoint tests
- `test_500mb_processing.py` - Large file handling

### `/e2e/`
End-to-end tests:
- `test_chatbot_comprehensive.py` - Complete chatbot workflow
- `test_application.py` - Full application tests

## Running Tests

### All Tests
```bash
pytest tests/
```

### Unit Tests Only
```bash
pytest tests/unit/
```

### Integration Tests
```bash
pytest tests/integration/
```

### E2E Tests
```bash
pytest tests/e2e/
```

### With Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Specific Test File
```bash
pytest tests/integration/test_document_ingestion_final.py -v
```

## Test Requirements

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Writing Tests

### Unit Test Example
```python
def test_ocr_service():
    from app.services.ocr_service import OCRService
    ocr_service = OCRService()
    result = ocr_service.extract_text("test.pdf")
    assert result is not None
```

### Integration Test Example
```python
def test_document_upload(client):
    response = client.post('/api/upload', 
                          data={'file': open('test.pdf', 'rb')})
    assert response.status_code == 200
```

## CI/CD Integration

Tests run automatically on:
- Pull requests
- Commits to main branch
- Pre-deployment validation

See `.github/workflows/tests.yml` for CI configuration.
