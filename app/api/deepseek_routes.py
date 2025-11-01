"""
API endpoints for DeepSeek OCR management
"""

from flask import Blueprint, jsonify, request
from app.services.deepseek_ocr_manager import deepseek_manager
from app.services.ocr_service import OCRService
import pytesseract
from PIL import Image
import io
import base64

deepseek_bp = Blueprint('deepseek', __name__)

@deepseek_bp.route('/api/deepseek/start', methods=['POST'])
def start_deepseek_server():
    """Start the DeepSeek OCR server"""
    try:
        success = deepseek_manager.start_server()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'DeepSeek OCR server started successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to start DeepSeek OCR server'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting DeepSeek OCR server: {str(e)}'
        }), 500

@deepseek_bp.route('/api/deepseek/stop', methods=['POST'])
def stop_deepseek_server():
    """Stop the DeepSeek OCR server"""
    try:
        deepseek_manager.stop_server()
        
        return jsonify({
            'success': True,
            'message': 'DeepSeek OCR server stopped successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error stopping DeepSeek OCR server: {str(e)}'
        }), 500

@deepseek_bp.route('/api/deepseek/status', methods=['GET'])
def get_deepseek_status():
    """Get the status of the DeepSeek OCR server"""
    try:
        is_running = deepseek_manager.check_server_status()
        server_info = deepseek_manager.get_server_info()
        
        return jsonify({
            'success': True,
            'is_running': is_running,
            'message': 'Server is running' if is_running else 'Server is not running',
            'server_info': server_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'is_running': False,
            'message': f'Error checking server status: {str(e)}'
        }), 500

@deepseek_bp.route('/api/ocr/test-tesseract', methods=['POST'])
def test_tesseract_ocr():
    """Test Tesseract OCR functionality"""
    try:
        # Create a simple test image with text
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a white image with black text
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font, fallback if not available
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
            
        draw.text((10, 30), "Test OCR Text", fill='black', font=font)
        
        # Test with Tesseract
        text = pytesseract.image_to_string(img)
        
        if 'Test' in text or 'OCR' in text:
            return jsonify({
                'success': True,
                'message': 'Tesseract OCR is working correctly',
                'extracted_text': text.strip()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Tesseract OCR test failed - no text extracted',
                'extracted_text': text.strip()
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Tesseract OCR test failed: {str(e)}'
        }), 500

@deepseek_bp.route('/api/ocr/tesseract-languages', methods=['GET'])
def get_tesseract_languages():
    """Get available Tesseract languages"""
    try:
        from app.services.ocr_service import OCRService
        
        ocr_service = OCRService()
        languages = ocr_service.get_tesseract_languages()
        
        return jsonify({
            'success': True,
            'languages': languages,
            'message': f'Found {len(languages)} available languages'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting Tesseract languages: {str(e)}'
        }), 500

@deepseek_bp.route('/api/ocr/test-pipeline', methods=['POST'])
def test_ocr_pipeline():
    """Test the complete OCR pipeline"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a test image
        img = Image.new('RGB', (400, 150), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
            
        draw.text((20, 50), "OCR Pipeline Test", fill='black', font=font)
        
        results = {}
        ocr_service = OCRService()
        
        # Test DeepSeek Local
        try:
            deepseek_text = ocr_service._deepseek_ocr(img)
            results['deepseek_local'] = bool(deepseek_text and 'OCR' in deepseek_text)
        except Exception as e:
            results['deepseek_local'] = False
            results['deepseek_error'] = str(e)
        
        # Test Tesseract
        try:
            tesseract_text = ocr_service._tesseract_ocr(img)
            results['tesseract'] = bool(tesseract_text and 'OCR' in tesseract_text)
        except Exception as e:
            results['tesseract'] = False
            results['tesseract_error'] = str(e)
        
        # Check if any method worked
        success = any([results.get('deepseek_local'), results.get('tesseract')])
        
        return jsonify({
            'success': success,
            'message': 'OCR pipeline test completed',
            **results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'OCR pipeline test failed: {str(e)}'
        }), 500