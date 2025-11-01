"""
WSGI Entry Point for OCR Agent Pro
For use with production WSGI servers (Gunicorn, uWSGI, etc.)

Usage:
    gunicorn wsgi:application -w 4 -b 0.0.0.0:5000
    uwsgi --http :5000 --wsgi-file wsgi.py --callable application
"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Create the Flask application
application = create_app()

if __name__ == "__main__":
    # For development only - use server.py for production
    application.run(host='0.0.0.0', port=5000, debug=False)
