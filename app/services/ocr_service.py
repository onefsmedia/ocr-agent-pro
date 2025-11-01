import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import PyPDF2
import os
import requests
import base64
import io
import tempfile
from typing import Optional, Dict, Any, List
from flask import current_app
from .deepseek_service import DeepSeekOCRService

class OCRService:
    """Service for OCR processing of documents using DeepSeek OCR and Tesseract"""
    
    def __init__(self) -> None:
        # Initialize DeepSeek OCR Service
        self.deepseek_service = DeepSeekOCRService()
        
        # Store the correct Tesseract path as instance variable
        self.tesseract_cmd = None
        
        # Initialize Tesseract path with better debugging
        self._initialize_tesseract_path_debug()
        
        # Initialize configuration
        self.use_deepseek_ocr = True  # Default to using DeepSeek if available
        
        # Override with config if available
        try:
            if hasattr(current_app, 'config') and current_app.config.get('TESSERACT_PATH'):
                config_path = current_app.config['TESSERACT_PATH']
                if os.path.exists(config_path):
                    self.tesseract_cmd = config_path
                    pytesseract.pytesseract.tesseract_cmd = config_path
                    print(f"Using Tesseract from config: {config_path}")
        except:
            pass
    
    def _initialize_tesseract_path_debug(self):
        """Initialize Tesseract path with detailed debugging"""
        print("🔍 Initializing Tesseract path...")
        
        # Set Tesseract path - try multiple common locations
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        
        tesseract_found = False
        
        # First try the specific paths
        for path in tesseract_paths:
            print(f"  Checking: {path}")
            if os.path.exists(path):
                self.tesseract_cmd = path
                pytesseract.pytesseract.tesseract_cmd = path
                tesseract_found = True
                print(f"  ✅ Tesseract found at: {path}")
                print(f"  ✅ pytesseract.tesseract_cmd set to: {pytesseract.pytesseract.tesseract_cmd}")
                break
            else:
                print(f"  ❌ Not found: {path}")
        
        # If not found, try testing the default "tesseract" command
        if not tesseract_found:
            print("  Trying default 'tesseract' command...")
            try:
                import subprocess
                result = subprocess.run(['tesseract', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print("  ⚠️ WARNING: Using 'tesseract' command (may resolve to Unix path)")
                    self.tesseract_cmd = 'tesseract'
                    pytesseract.pytesseract.tesseract_cmd = 'tesseract'
                    tesseract_found = True
                    print(f"  tesseract command found in PATH, resolved to: {pytesseract.pytesseract.tesseract_cmd}")
            except Exception as e:
                print(f"  ❌ tesseract command failed: {e}")
        
        if not tesseract_found:
            print("  ❌ Warning: Tesseract not found. OCR will only use DeepSeek if available.")
        
        print(f"🎯 Final state: self.tesseract_cmd = {self.tesseract_cmd}")
        print(f"🎯 Final state: pytesseract.tesseract_cmd = {pytesseract.pytesseract.tesseract_cmd}")
        
        # DeepSeek OCR configuration with safe access to current_app
        try:
            self.deepseek_ocr_url: str = current_app.config.get('DEEPSEEK_OCR_URL', 'http://localhost:8001')
            self.use_deepseek_ocr: bool = current_app.config.get('USE_DEEPSEEK_OCR', True)
        except (RuntimeError, AttributeError):
            # Fallback when current_app is not available
            self.deepseek_ocr_url = 'http://localhost:8001'
            self.use_deepseek_ocr = True
        
        # Test Tesseract availability
        try:
            pytesseract.get_tesseract_version()
            self.tesseract_available: bool = True
        except Exception:
            self.tesseract_available = False
    
    def process_document_with_language(self, file_path: str, language: Optional[str] = None) -> str:
        """Process a document with specific language support"""
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self._process_pdf_with_language(file_path, language)
            elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                return self._process_image_with_language(file_path, language)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")

    def _process_image_with_language(self, file_path: str, language: Optional[str] = None) -> str:
        """Process image file with OCR and language support"""
        
        try:
            image = Image.open(file_path)
            
            # Use appropriate OCR method - prioritize DeepSeek OCR (supports multiple languages)
            if self._should_use_deepseek_ocr():
                return self._deepseek_ocr(image)
            elif self._should_use_tesseract():
                return self._tesseract_ocr(image, language)
            else:
                raise Exception("No OCR method available")
                
        except Exception as e:
            raise Exception(f"Image OCR failed: {str(e)}")

    def _process_pdf_with_language(self, file_path: str, language: Optional[str] = None) -> str:
        """Process PDF file with language support"""
        
        extracted_text = ""
        
        # First try to extract text directly from PDF
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text.strip():
                        extracted_text += text + "\n"
        except Exception as e:
            print(f"Direct PDF text extraction failed: {e}")
        
        # If no text extracted or minimal text, perform OCR on images
        if len(extracted_text.strip()) < 100:  # Threshold for minimal text
            try:
                # Convert PDF pages to images
                poppler_path = r"C:\Users\onefs\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin"
                images = convert_from_path(file_path, dpi=300, poppler_path=poppler_path)
                
                ocr_text = ""
                for i, image in enumerate(images):
                    # Use appropriate OCR method with language support
                    if self._should_use_deepseek_ocr():
                        page_text = self._deepseek_ocr(image)
                    elif self._should_use_tesseract():
                        page_text = self._tesseract_ocr(image, language)
                    else:
                        raise Exception("No OCR method available")
                    
                    if page_text.strip():
                        ocr_text += f"[Page {i+1}]\n{page_text}\n\n"
                
                if ocr_text.strip():
                    extracted_text = ocr_text
                else:
                    raise Exception("Both text extraction and OCR failed for PDF")
            except Exception as e:
                raise Exception(f"PDF OCR processing failed: {str(e)}")
        
        return extracted_text.strip()

    def process_document(self, file_path: str) -> str:
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self._process_pdf(file_path)
            elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                return self._process_image(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def _process_pdf(self, file_path: str) -> str:
        """Process PDF file - extract text and perform OCR on images"""
        
        extracted_text = ""
        
        # First try to extract text directly from PDF
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text.strip():
                        extracted_text += text + "\n"
        except Exception as e:
            print(f"Direct PDF text extraction failed: {e}")
        
        # If no text extracted or minimal text, perform OCR on images
        if len(extracted_text.strip()) < 100:  # Threshold for minimal text
            try:
                # Convert PDF pages to images
                poppler_path = r"C:\Users\onefs\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin"
                images = convert_from_path(file_path, dpi=300, poppler_path=poppler_path)
                
                ocr_text = ""
                for i, image in enumerate(images):
                    # Use appropriate OCR method - prioritize DeepSeek OCR
                    if self._should_use_deepseek_ocr():
                        page_text = self._deepseek_ocr(image)
                    elif self._should_use_tesseract():
                        page_text = self._tesseract_ocr(image)
                    else:
                        raise Exception("No OCR method available")
                    
                    ocr_text += f"\n--- Page {i+1} ---\n{page_text}\n"
                
                # Use OCR text if it's more substantial
                if len(ocr_text.strip()) > len(extracted_text.strip()):
                    extracted_text = ocr_text
                    
            except Exception as e:
                print(f"PDF OCR failed: {e}")
                if not extracted_text.strip():
                    raise Exception("Both text extraction and OCR failed for PDF")
        
        return extracted_text.strip()
    
    def _process_image(self, file_path: str) -> str:
        """Process image file with OCR"""
        
        try:
            image = Image.open(file_path)
            
            # Use appropriate OCR method - prioritize DeepSeek OCR
            if self._should_use_deepseek_ocr():
                return self._deepseek_ocr(image)
            elif self._should_use_tesseract():
                return self._tesseract_ocr(image)
            else:
                raise Exception("No OCR method available")
                
        except Exception as e:
            raise Exception(f"Image OCR failed: {str(e)}")
    
    def _tesseract_ocr(self, image: Image.Image, language: Optional[str] = None) -> str:
        """Perform OCR using Tesseract with language detection and French support"""
        
        try:
            # Force set the correct Tesseract path each time
            if self.tesseract_cmd:
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
                print(f"Debug: Using Tesseract path: {self.tesseract_cmd}")
            else:
                # Re-initialize path if somehow lost
                self._initialize_tesseract_path()
                if self.tesseract_cmd:
                    pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
            
            # Get available languages
            available_langs = self.get_tesseract_languages()
            print(f"Debug: Available languages: {available_langs}")
            
            # Determine language configuration for Cameroon (English + French)
            if language:
                lang_config = language
            else:
                # For Cameroon, try French first, then English, then combined
                if 'fra' in available_langs:
                    # Try French + English combination for Cameroon
                    lang_config = 'fra+eng'
                    print("Using French + English language combination for Cameroon")
                else:
                    # Fallback to English only if French not available
                    lang_config = 'eng'
                    print("French language pack not available, using English only")
                    print("💡 To add French support, install the French language pack:")
                    print("   Download fra.traineddata from GitHub and place in tessdata folder")
            
            # Configure Tesseract for better accuracy with selected language(s)
            custom_config = f'--oem 3 --psm 6 -l {lang_config}'
            text = pytesseract.image_to_string(image, config=custom_config)
            
            print(f"Debug: OCR completed with language(s): {lang_config}")
            return text.strip()
            
        except Exception as e:
            # If French+English fails, try English only as fallback
            if language is None and 'fra+eng' in locals().get('lang_config', ''):
                print("French+English combination failed, falling back to English only")
                try:
                    custom_config = r'--oem 3 --psm 6 -l eng'
                    text = pytesseract.image_to_string(image, config=custom_config)
                    return text.strip()
                except Exception as fallback_e:
                    raise Exception(f"Tesseract OCR failed (both multilingual and English): {str(fallback_e)}")
            
            raise Exception(f"Tesseract OCR failed: {str(e)}")
    
    def _initialize_tesseract_path(self):
        """Initialize Tesseract path - separate method for reuse"""
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        
        for path in tesseract_paths:
            if os.path.exists(path):
                self.tesseract_cmd = path
                pytesseract.pytesseract.tesseract_cmd = path
                print(f"Tesseract initialized at: {path}")
                return True
        
        return False
    
    def get_tesseract_languages(self) -> List[str]:
        """Get available Tesseract languages"""
        try:
            # Ensure Tesseract path is set
            if self.tesseract_cmd:
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
            else:
                self._initialize_tesseract_path()
            
            languages = pytesseract.get_languages()
            return languages
        except Exception as e:
            raise Exception(f"Error getting Tesseract languages: {str(e)}")
    
    def _deepseek_ocr(self, image: Image.Image) -> str:
        """Perform OCR using DeepSeek OCR local installation"""
        
        try:
            # Save PIL image to temporary file
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                image.save(temp_file.name, format='PNG')
                temp_path = temp_file.name
            
            try:
                # Use our new DeepSeek service
                success, result_text, error_msg = self.deepseek_service.process_image(temp_path)
                
                if success:
                    print("DeepSeek OCR processed successfully")
                    return result_text
                else:
                    print(f"DeepSeek OCR failed: {error_msg}")
                    # Fallback to API method
                    return self._deepseek_ocr_api(image)
                    
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
        except Exception as e:
            print(f"DeepSeek OCR local processing error: {e}")
            # Fallback to API method
            return self._deepseek_ocr_api(image)
    
    def _deepseek_ocr_api(self, image: Image.Image, img_base64: Optional[str] = None) -> str:
        """Perform OCR using DeepSeek OCR API (fallback method)"""
        
        try:
            # Convert PIL image to base64 if not provided
            if not img_base64:
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
            
            # Prepare request payload for DeepSeek OCR
            payload = {
                "image": img_base64,
                "format": "png",
                "options": {
                    "language": "auto",
                    "extract_tables": True,
                    "extract_equations": True,
                    "preserve_layout": True
                }
            }
            
            # Send request to DeepSeek OCR API
            response = requests.post(
                f"{self.deepseek_ocr_url}/api/ocr",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract text from DeepSeek OCR response
                if 'text' in result:
                    return result['text']
                elif 'content' in result:
                    return result['content']
                elif 'extracted_text' in result:
                    return result['extracted_text']
                else:
                    # Try to extract from structured response
                    text_parts = []
                    if 'blocks' in result:
                        for block in result['blocks']:
                            if 'text' in block:
                                text_parts.append(block['text'])
                    return '\n'.join(text_parts) if text_parts else ""
            else:
                raise Exception(f"DeepSeek OCR API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"DeepSeek OCR API fallback error: {e}")
            # Final fallback to Tesseract
            return self._tesseract_ocr(image)
        except requests.exceptions.ConnectionError:
            raise Exception("DeepSeek OCR service not available. Please ensure the service is running.")
        except requests.exceptions.Timeout:
            raise Exception("DeepSeek OCR request timed out")
        except Exception as e:
            raise Exception(f"DeepSeek OCR failed: {str(e)}")
    
    def _should_use_deepseek_ocr(self) -> bool:
        """Determine whether to use DeepSeek OCR"""
        
        if not hasattr(current_app, 'config'):
            return False
            
        return (self.use_deepseek_ocr and 
                self._test_deepseek_connection())
    
    def _should_use_tesseract(self) -> bool:
        """Determine whether Tesseract is available"""
        
        try:
            # Ensure we have the correct Tesseract path set from our stored value
            if self.tesseract_cmd:
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd
            else:
                # Try to find Tesseract again if we don't have a stored path
                tesseract_paths = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                ]
                
                for path in tesseract_paths:
                    if os.path.exists(path):
                        self.tesseract_cmd = path
                        pytesseract.pytesseract.tesseract_cmd = path
                        break
            
            # Test if Tesseract is available
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False
    
    def _test_deepseek_connection(self) -> bool:
        """Test connection to DeepSeek OCR service"""
        
        try:
            response = requests.get(
                f"{self.deepseek_ocr_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def get_document_info(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata and basic info from document"""
        
        file_stats = os.stat(file_path)
        file_extension = os.path.splitext(file_path)[1].lower()
        
        info = {
            'file_size': file_stats.st_size,
            'file_type': file_extension,
            'created_at': file_stats.st_ctime,
            'modified_at': file_stats.st_mtime
        }
        
        if file_extension == '.pdf':
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    info['page_count'] = len(pdf_reader.pages)
                    
                    # Try to get PDF metadata
                    if pdf_reader.metadata:
                        info['title'] = pdf_reader.metadata.get('/Title', '')
                        info['author'] = pdf_reader.metadata.get('/Author', '')
                        info['subject'] = pdf_reader.metadata.get('/Subject', '')
                        info['creator'] = pdf_reader.metadata.get('/Creator', '')
                        
            except Exception as e:
                print(f"Could not extract PDF metadata: {e}")
        
        elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            try:
                with Image.open(file_path) as img:
                    info['dimensions'] = img.size
                    info['mode'] = img.mode
                    info['format'] = img.format
                    
                    # Get EXIF data if available
                    if hasattr(img, '_getexif') and img._getexif():
                        info['exif'] = dict(img._getexif())
                        
            except Exception as e:
                print(f"Could not extract image metadata: {e}")
        
        return info