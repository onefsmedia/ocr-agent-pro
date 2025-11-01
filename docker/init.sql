-- Database initialization script for OCR Agent
-- This script will be run when the PostgreSQL container starts

-- Note: pgvector extension is not required for basic functionality
-- CREATE EXTENSION IF NOT EXISTS vector;

-- Grant permissions to the database user
GRANT ALL PRIVILEGES ON DATABASE ocr_agent TO renderman;

-- Note: Tables will be created by the Flask application using SQLAlchemy
-- The Flask app will run db.create_all() on startup