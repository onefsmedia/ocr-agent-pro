"""
API routes for prompt management functionality
"""
from flask import Blueprint, request, jsonify, current_app
from app.models import SystemSettings, db
from sqlalchemy.exc import SQLAlchemyError
import json
import logging

# Create blueprint
prompt_api = Blueprint('prompt_api', __name__, url_prefix='/api/prompts')

# Configure logging
logger = logging.getLogger(__name__)

@prompt_api.route('/', methods=['GET'])
def get_prompts():
    """Get all prompt templates"""
    try:
        # Get system prompts from settings
        prompts = SystemSettings.query.filter(
            SystemSettings.key.like('%prompt%')
        ).all()
        
        prompt_data = []
        for prompt in prompts:
            prompt_data.append({
                'id': prompt.id,
                'key': prompt.key,
                'name': prompt.key.replace('_', ' ').title(),
                'value': prompt.value,
                'description': prompt.description,
                'type': prompt.setting_type,
                'updated_at': prompt.updated_at.isoformat() if prompt.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'prompts': prompt_data
        })
        
    except Exception as e:
        logger.error(f"Error getting prompts: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_api.route('/save', methods=['POST'])
def save_prompt():
    """Save or update a prompt template"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        required_fields = ['key', 'value']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Check if prompt exists
        existing_prompt = SystemSettings.query.filter_by(key=data['key']).first()
        
        if existing_prompt:
            # Update existing prompt
            existing_prompt.value = data['value']
            if 'description' in data:
                existing_prompt.description = data['description']
        else:
            # Create new prompt
            new_prompt = SystemSettings(
                key=data['key'],
                value=data['value'],
                description=data.get('description', f"Custom prompt: {data['key']}"),
                setting_type='string'
            )
            db.session.add(new_prompt)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prompt saved successfully'
        })
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error saving prompt: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Database error occurred'
        }), 500
    except Exception as e:
        logger.error(f"Error saving prompt: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_api.route('/test', methods=['POST'])
def test_prompt():
    """Test a prompt with sample input"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                'success': False,
                'error': 'No prompt provided'
            }), 400
        
        prompt_content = data['prompt']
        sample_input = data.get('sample_input', 'This is a test document for prompt validation.')
        
        # Simple prompt validation
        test_result = {
            'prompt_length': len(prompt_content),
            'has_variables': any(var in prompt_content for var in ['{document_content}', '{user_query}', '{context}']),
            'sample_output': f"Test response for prompt: {prompt_content[:100]}..." if len(prompt_content) > 100 else prompt_content
        }
        
        return jsonify({
            'success': True,
            'test_result': test_result,
            'message': 'Prompt test completed'
        })
        
    except Exception as e:
        logger.error(f"Error testing prompt: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_api.route('/<int:prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    """Delete a prompt template"""
    try:
        prompt = SystemSettings.query.get(prompt_id)
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt not found'
            }), 404
        
        # Don't allow deletion of core system prompts
        protected_keys = ['system_prompt', 'default_prompt']
        if prompt.key in protected_keys:
            return jsonify({
                'success': False,
                'error': 'Cannot delete protected system prompt'
            }), 403
        
        db.session.delete(prompt)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prompt deleted successfully'
        })
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error deleting prompt: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Database error occurred'
        }), 500
    except Exception as e:
        logger.error(f"Error deleting prompt: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_api.route('/categories', methods=['GET'])
def get_prompt_categories():
    """Get available prompt categories"""
    try:
        categories = [
            {'id': 'system', 'name': 'System', 'icon': 'fas fa-robot', 'description': 'Core system behavior prompts'},
            {'id': 'ocr', 'name': 'OCR', 'icon': 'fas fa-eye', 'description': 'OCR processing and analysis'},
            {'id': 'chat', 'name': 'Chat', 'icon': 'fas fa-comments', 'description': 'Interactive chat responses'},
            {'id': 'analysis', 'name': 'Analysis', 'icon': 'fas fa-search', 'description': 'Document analysis and insights'},
            {'id': 'lesson', 'name': 'Lesson', 'icon': 'fas fa-graduation-cap', 'description': 'Educational content generation'}
        ]
        
        return jsonify({
            'success': True,
            'categories': categories
        })
        
    except Exception as e:
        logger.error(f"Error getting prompt categories: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@prompt_api.route('/defaults', methods=['POST'])
def reset_to_defaults():
    """Reset prompts to default values"""
    try:
        # Default prompts
        default_prompts = {
            'system_prompt': {
                'value': 'You are a helpful AI assistant specialized in document analysis and OCR. You provide accurate, helpful responses based on the content of uploaded documents.',
                'description': 'Default system prompt for the AI chatbot'
            },
            'ocr_prompt': {
                'value': 'Analyze the following OCR extracted text and provide corrections, insights, and structure improvements:\n\n{ocr_text}\n\nFocus on accuracy, readability, and identifying any potential OCR errors.',
                'description': 'OCR text analysis and correction prompt'
            },
            'chat_prompt': {
                'value': 'You are an intelligent document assistant. Answer user questions based on the provided document context:\n\nContext: {context}\nUser Question: {user_query}\n\nProvide a helpful, accurate response.',
                'description': 'Interactive chat responses prompt'
            },
            'analysis_prompt': {
                'value': 'Perform a comprehensive analysis of the following document:\n\n{document_content}\n\nProvide insights on:\n1. Key topics and themes\n2. Important information\n3. Structure and organization\n4. Recommendations',
                'description': 'Deep document analysis prompt'
            },
            'lesson_prompt': {
                'value': 'Create comprehensive lesson notes based on the following content:\n\n{content}\n\nGenerate:\n1. Learning objectives\n2. Key concepts\n3. Detailed explanations\n4. Examples and activities\n5. Assessment questions',
                'description': 'Educational content creation prompt'
            }
        }
        
        # Update or create default prompts
        for key, prompt_data in default_prompts.items():
            existing = SystemSettings.query.filter_by(key=key).first()
            
            if existing:
                existing.value = prompt_data['value']
                existing.description = prompt_data['description']
            else:
                new_prompt = SystemSettings(
                    key=key,
                    value=prompt_data['value'],
                    description=prompt_data['description'],
                    setting_type='string'
                )
                db.session.add(new_prompt)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prompts reset to defaults successfully'
        })
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error resetting prompts: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Database error occurred'
        }), 500
    except Exception as e:
        logger.error(f"Error resetting prompts: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500