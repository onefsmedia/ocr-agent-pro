"""
API routes for lesson note generation
"""

from flask import Blueprint, request, jsonify
from app.services.lesson_service import LessonNoteService
from app.services.onlyoffice_api import onlyoffice_api
from app.models import db, Document
from sqlalchemy import text

lesson_bp = Blueprint('lessons', __name__)

@lesson_bp.route('/api/lessons/check-documents', methods=['POST'])
def check_documents():
    """Check available documents for subject and class"""
    try:
        data = request.get_json()
        subject = data.get('subject')
        class_level = data.get('class_level')
        
        if not subject or not class_level:
            return jsonify({
                'success': False,
                'error': 'Subject and class level are required'
            }), 400
        
        # Count documents by type
        query = text("""
            SELECT 
                COUNT(CASE WHEN metadata->>'type' = 'textbook' OR metadata->>'type' IS NULL THEN 1 END) as documents_count,
                COUNT(CASE WHEN metadata->>'type' = 'curriculum' THEN 1 END) as curriculum_count,
                COUNT(CASE WHEN metadata->>'type' = 'progression' THEN 1 END) as progression_count
            FROM documents 
            WHERE (metadata->>'class') = :class_level 
            AND (metadata->>'subject') = :subject
        """)
        
        result = db.session.execute(query, {
            'class_level': class_level,
            'subject': subject
        }).fetchone()
        
        return jsonify({
            'success': True,
            'documents_count': result[0] or 0,
            'curriculum_count': result[1] or 0,
            'progression_count': result[2] or 0,
            'subject': subject,
            'class_level': class_level
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lesson_bp.route('/api/lessons/load', methods=['POST'])
def load_lessons():
    """Load lessons for subject and class"""
    try:
        data = request.get_json()
        subject = data.get('subject')
        class_level = data.get('class_level')
        
        if not subject or not class_level:
            return jsonify({
                'success': False,
                'error': 'Subject and class level are required'
            }), 400
        
        lesson_service = LessonNoteService()
        
        # Get subject documents
        documents_data = lesson_service.get_subject_documents(subject, class_level)
        
        if not documents_data:
            return jsonify({
                'success': False,
                'error': 'No documents found for this subject and class'
            }), 404
        
        # Extract lesson titles from progression documents
        progression_docs = documents_data.get('progression_documents', [])
        
        if not progression_docs:
            return jsonify({
                'success': False,
                'error': 'No progression documents found. Please upload curriculum progression data.'
            }), 404
        
        lessons = lesson_service.extract_lesson_titles(progression_docs)
        
        if not lessons:
            return jsonify({
                'success': False,
                'error': 'No lessons could be extracted from progression documents'
            }), 404
        
        return jsonify({
            'success': True,
            'lessons': lessons,
            'subject': subject,
            'class_level': class_level,
            'total_lessons': len(lessons)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lesson_bp.route('/api/lessons/generate', methods=['POST'])
def generate_lesson():
    """Generate a single lesson note"""
    try:
        data = request.get_json()
        subject = data.get('subject')
        class_level = data.get('class_level')
        lesson_info = data.get('lesson')
        
        if not all([subject, class_level, lesson_info]):
            return jsonify({
                'success': False,
                'error': 'Subject, class level, and lesson information are required'
            }), 400
        
        lesson_service = LessonNoteService()
        
        # Get subject documents
        documents_data = lesson_service.get_subject_documents(subject, class_level)
        
        if not documents_data:
            return jsonify({
                'success': False,
                'error': 'No documents found for this subject and class'
            }), 404
        
        # Generate lesson note using AI
        lesson_note = lesson_service.generate_lesson_note(
            subject=subject,
            class_level=class_level,
            lesson_info=lesson_info,
            documents=documents_data.get('documents', []),
            curriculum=documents_data.get('curriculum_documents', [])
        )
        
        if 'error' in lesson_note:
            return jsonify({
                'success': False,
                'error': lesson_note['error']
            }), 500
        
        # Create OnlyOffice document
        onlyoffice_result = lesson_service.create_onlyoffice_document(lesson_note)
        
        if not onlyoffice_result.get('success'):
            return jsonify({
                'success': False,
                'error': f"Failed to create OnlyOffice document: {onlyoffice_result.get('error')}"
            }), 500
        
        # Store lesson information in database
        lesson_data = {
            'title': lesson_note.get('lessonTitle', 'Untitled Lesson'),
            'content': lesson_note.get('mainBody', ''),
            'subject': subject,
            'class_level': class_level,
            'document_id': onlyoffice_result['document_id'],
            'document_url': onlyoffice_result['document_url']
        }
        
        storage_success = lesson_service.store_lesson_info(lesson_data)
        
        if not storage_success:
            print("Warning: Failed to store lesson info in database")
        
        return jsonify({
            'success': True,
            'title': lesson_note.get('lessonTitle', 'Untitled Lesson'),
            'document_id': onlyoffice_result['document_id'],
            'edit_url': onlyoffice_result['document_url'],
            'download_url': onlyoffice_result['download_url'],
            'view_url': onlyoffice_result.get('view_url', onlyoffice_result['document_url']),
            'lesson_note': lesson_note
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lesson_bp.route('/api/lessons/generated', methods=['POST'])
def get_generated_lessons():
    """Get previously generated lessons for subject and class"""
    try:
        data = request.get_json()
        subject = data.get('subject')
        class_level = data.get('class_level')
        
        if not subject or not class_level:
            return jsonify({
                'success': False,
                'error': 'Subject and class level are required'
            }), 400
        
        # Query database for generated lesson notes
        lessons = Document.query.filter(
            Document.file_type == 'lesson_note',
            Document.metadata['subject'].astext == subject,
            Document.metadata['class'].astext == class_level
        ).all()
        
        lesson_list = []
        for lesson in lessons:
            lesson_data = {
                'lesson_title': lesson.metadata.get('lesson_title', 'Untitled Lesson'),
                'document_id': lesson.metadata.get('document_id'),
                'edit_url': lesson.metadata.get('document_url'),
                'download_url': f"/api/documents/{lesson.id}/download",
                'view_url': lesson.metadata.get('document_url'),
                'generated_at': lesson.created_at.isoformat() if lesson.created_at else None,
                'status': lesson.metadata.get('status', 'unknown')
            }
            lesson_list.append(lesson_data)
        
        return jsonify({
            'success': True,
            'lessons': lesson_list,
            'total': len(lesson_list),
            'subject': subject,
            'class_level': class_level
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lesson_bp.route('/api/onlyoffice/status', methods=['GET'])
def check_onlyoffice_status():
    """Check OnlyOffice server status"""
    try:
        status = onlyoffice_api.check_server_status()
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'error',
            'message': str(e)
        }), 500

@lesson_bp.route('/api/onlyoffice/config/<doc_id>', methods=['GET'])
def get_editor_config(doc_id):
    """Get OnlyOffice editor configuration for a document"""
    try:
        title = request.args.get('title', f'Document {doc_id}')
        mode = request.args.get('mode', 'edit')
        
        config = onlyoffice_api.get_editor_config(doc_id, title, mode)
        
        if config:
            return jsonify({
                'success': True,
                'config': config
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate editor configuration'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@lesson_bp.route('/api/documents/<int:doc_id>/download', methods=['GET'])
def download_document(doc_id):
    """Download a generated document"""
    try:
        document = Document.query.get_or_404(doc_id)
        
        # For now, return the content as text
        # In a real implementation, you'd return the actual DOCX file
        return jsonify({
            'success': True,
            'content': document.content,
            'filename': document.filename,
            'title': document.metadata.get('lesson_title', 'Untitled Lesson')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500