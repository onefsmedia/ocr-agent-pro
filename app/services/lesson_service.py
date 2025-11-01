"""
Lesson Note Generation Service
Handles AI-powered lesson note creation with OnlyOffice integration
"""

import requests
import json
import uuid
from typing import Dict, Any, List, Optional
from flask import current_app
from ..models import db, Document, DocumentChunk
from sqlalchemy import text

class LessonNoteService:
    """Service for generating lesson notes using AI and OnlyOffice"""
    
    def __init__(self):
        # Get settings from database or use defaults
        self._load_ai_settings()
        
    def _load_ai_settings(self):
        """Load AI/LLM settings from database"""
        try:
            from app.models import SystemSettings
            
            # Get settings from database
            settings = {s.key: s.value for s in SystemSettings.query.all()}
            
            self.onlyoffice_url = current_app.config.get('ONLYOFFICE_URL', 'http://localhost:8000')
            self.ollama_url = settings.get('llm_base_url', 'http://localhost:11434')
            self.ollama_model = settings.get('llm_model', 'llama3.3:latest')
            self.temperature = float(settings.get('llm_temperature', '0.7'))
            self.max_tokens = int(settings.get('llm_max_tokens', '2048'))
            self.provider = settings.get('llm_provider', 'ollama')
            
        except Exception as e:
            # Fallback to defaults if database is not available
            print(f"Warning: Could not load AI settings from database: {e}")
            self.onlyoffice_url = current_app.config.get('ONLYOFFICE_URL', 'http://localhost:8000')
            self.ollama_url = current_app.config.get('OLLAMA_BASE_URL', 'http://localhost:11434')
            self.ollama_model = current_app.config.get('OLLAMA_MODEL', 'llama3.3:latest')
            self.temperature = 0.7
            self.max_tokens = 2048
            self.provider = 'ollama'
        
    def get_subject_documents(self, subject: str, class_level: str) -> Dict[str, Any]:
        """Retrieve documents for a specific subject and class"""
        try:
            # Build the query to get documents, progression, and curriculum
            query = text("""
                SELECT json_build_object(
                  'documents', (
                    SELECT json_agg(json_build_object(
                        'content', content,
                        'metadata', metadata
                    ))
                    FROM documents
                    WHERE (metadata->>'class') = :class_level
                      AND (metadata->>'subject') = :subject
                  ),
                  'progression_documents', (
                    SELECT json_agg(json_build_object('lesson', trim(value)))
                    FROM (
                      SELECT unnest(string_to_array(content, E'\\n')) AS value
                      FROM documents
                      WHERE (metadata->>'class') = :class_level
                        AND (metadata->>'subject') = :subject
                        AND (metadata->>'type') = 'progression'
                    ) t
                    WHERE value <> ''
                  ),
                  'curriculum_documents', (
                    SELECT json_agg(json_build_object(
                        'content', content,
                        'metadata', metadata
                    ))
                    FROM documents
                    WHERE (metadata->>'class') = :class_level
                      AND (metadata->>'subject') = :subject
                      AND (metadata->>'type') = 'curriculum'
                  )
                ) AS result
            """)
            
            result = db.session.execute(query, {
                'class_level': class_level,
                'subject': subject
            }).fetchone()
            
            return result[0] if result else {}
            
        except Exception as e:
            print(f"Error retrieving subject documents: {e}")
            return {}
    
    def extract_lesson_titles(self, progression_data: List[Dict]) -> List[Dict]:
        """Extract lesson titles from progression documents using AI"""
        try:
            if not progression_data:
                return []
            
            # Combine all lessons into a single text
            lessons_text = "\n".join([lesson.get('lesson', '') for lesson in progression_data])
            
            # AI prompt for lesson extraction
            system_prompt = """You are an expert curriculum data extractor.

Your task is to extract every lesson title from the given text and return them as a structured array.

Follow these rules strictly:
1. Identify each lesson title clearly.
2. Number them sequentially starting from 1.
3. Each lesson must follow this format: Lesson {number}: {title}
4. Output must be a valid JSON array.
5. Each item in the array must be an object like this: { "lesson": "Lesson 1: Introduction to Communication" }
6. Do not include explanations, markdown, or extra text.
7. Only return the clean JSON array.

Example output:
[
  { "lesson": "Lesson 1: Introduction to Communication" },
  { "lesson": "Lesson 2: At the Supermarket" },
  { "lesson": "Lesson 3: Making New Friends" }
]"""

            # Use Ollama for AI processing
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": lessons_text}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_ctx": 2048
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('message', {}).get('content', '')
                
                # Parse JSON response
                try:
                    lessons = json.loads(content)
                    return lessons if isinstance(lessons, list) else []
                except json.JSONDecodeError:
                    print("Failed to parse AI response as JSON")
                    return []
            else:
                print(f"Ollama API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error extracting lesson titles: {e}")
            return []
    
    def generate_lesson_note(self, subject: str, class_level: str, lesson_info: Dict, 
                           documents: List[Dict], curriculum: List[Dict]) -> Dict[str, Any]:
        """Generate a complete lesson note using AI"""
        try:
            # Prepare document content
            doc_content = "\n".join([doc.get('content', '') for doc in documents])
            curriculum_content = "\n".join([cur.get('content', '') for cur in curriculum])
            
            # AI prompt for lesson note generation
            system_prompt = f"""You are an expert {subject} teacher for {class_level} students.

Your task is to generate a **complete lesson note** for each lesson, strictly following the required structure.
The lesson must be based on:
1. The **curriculum objectives, methodology, and evaluation criteria**.
2. The **textbook content provided as input**.

### Output Requirements:
- Follow the **Sample Lesson Note Format** exactly (no extra text).
- Always contextualize with simple real-life examples.
- Use clear, teacher-friendly and student-friendly language.
- Do not skip any section, even if the textbook text is short.

### Mandatory Lesson Note Template

**Subject:** {subject}
**Class:** {class_level}
**Main Topic:** [From curriculum/textbook]
**Sub-topic:** [From curriculum/textbook]

**Presenter's Introduction**
Write a short, engaging introduction in a conversational tone. Mention why the topic is important in daily life.

**Lesson Outline**
- Clear definition(s) of key concept(s).
- Bullet points for key details.
- Step-by-step explanation of textbook content.
- Real-life examples.

**Units / Key Terms (if applicable)**
List and explain all relevant units, formulas, or terminology.

**Examples of [Concept] in Everyday Life**
Give at least 3–4 relatable examples drawn from students' environment.

**Animations / Visual Aids (if any)**
Describe what to show:
- Simple diagrams, charts, or animations.
- Everyday objects for illustration.

**Multiple Choice Questions (MCQs)**
Provide at least 5 MCQs with 3 options each (A, B, C).
Always state the correct answer.

**Closing**
A short wrap-up, reinforcing key ideas. End with motivation to observe the concept in real life and a link to the next lesson.

### Output Format Instruction

Return the entire lesson as **valid JSON** with this structure:

{{
  "subject": "{subject}",
  "classLevel": "{class_level}",
  "lessonTitle": "[lesson title]",
  "mainTopic": "[main topic]",
  "subTopic": "[sub topic]",
  "mainBody": "Full lesson text following the above structure (without markdown symbols)."
}}

Do **not** include any text outside the JSON object.
Ensure `mainBody` contains the formatted lesson note exactly as per the structure."""

            user_content = f"""subject: {doc_content}
curriculum: {curriculum_content}
lesson: {lesson_info.get('lesson', '')}"""

            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_ctx": 4096
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('message', {}).get('content', '')
                
                # Parse JSON response
                try:
                    lesson_note = json.loads(content)
                    return lesson_note
                except json.JSONDecodeError:
                    print("Failed to parse AI lesson note as JSON")
                    return {"error": "Failed to parse lesson note"}
            else:
                print(f"Ollama API error: {response.status_code}")
                return {"error": "Ollama API failed"}
                
        except Exception as e:
            print(f"Error generating lesson note: {e}")
            return {"error": str(e)}
    
    def save_lesson_note_locally(self, lesson_note: Dict[str, Any], output_dir: str = 'lesson_notes') -> str:
        """Save lesson note as local file when OnlyOffice is not available"""
        try:
            import os
            from datetime import datetime
            
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            subject = lesson_note.get('subject', 'lesson').replace(' ', '_')
            lesson_title = lesson_note.get('lessonTitle', 'note').replace(' ', '_')
            filename = f"{subject}_{lesson_title}_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # Format lesson content
            content = f"""LESSON NOTE
=====================================

Subject: {lesson_note.get('subject', 'N/A')}
Class Level: {lesson_note.get('classLevel', 'N/A')}
Main Topic: {lesson_note.get('mainTopic', 'N/A')}
Sub-topic: {lesson_note.get('subTopic', 'N/A')}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=====================================

{lesson_note.get('mainBody', 'No content available')}

=====================================
Generated by OCR Agent - Lesson Note Generator
"""
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
            
        except Exception as e:
            raise Exception(f"Failed to save lesson note locally: {str(e)}")
    
    def create_lesson_with_fallback(self, subject: str, class_level: str, lesson_info: Dict,
                                  documents: List[Dict], curriculum: List[Dict]) -> Dict[str, Any]:
        """Create lesson note with OnlyOffice fallback to local files"""
        try:
            # Generate the lesson note content
            lesson_note = self.generate_lesson_note(subject, class_level, lesson_info, documents, curriculum)
            
            if "error" in lesson_note:
                return lesson_note
            
            # Try OnlyOffice first
            try:
                from app.services.onlyoffice_service import OnlyOfficeService
                onlyoffice = OnlyOfficeService()
                
                # Check if OnlyOffice is available
                if onlyoffice.check_connection():
                    # Create document in OnlyOffice
                    title = f"{lesson_note.get('subject', 'Lesson')} - {lesson_note.get('lessonTitle', 'Note')}"
                    content = lesson_note.get('mainBody', '')
                    
                    document_id = onlyoffice.create_text_document(title, content)
                    
                    return {
                        "success": True,
                        "lesson_note": lesson_note,
                        "storage_type": "onlyoffice",
                        "document_id": document_id,
                        "message": "Lesson note created in OnlyOffice successfully"
                    }
                else:
                    raise Exception("OnlyOffice service not available")
                    
            except Exception as e:
                print(f"OnlyOffice creation failed: {e}")
                # Fallback to local file
                local_filepath = self.save_lesson_note_locally(lesson_note)
                
                return {
                    "success": True,
                    "lesson_note": lesson_note,
                    "storage_type": "local",
                    "file_path": local_filepath,
                    "message": f"OnlyOffice unavailable. Lesson note saved locally: {local_filepath}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate lesson note"
            }
    
    def create_onlyoffice_document(self, lesson_note: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new document in OnlyOffice and populate with lesson content"""
        try:
            # Generate unique document ID
            doc_id = str(uuid.uuid4())
            
            # Prepare document content
            content = f"""Class: {lesson_note.get('classLevel', '')}
Subject: {lesson_note.get('subject', '')}
{lesson_note.get('lessonTitle', '')}

{lesson_note.get('mainBody', '')}"""
            
            # OnlyOffice document creation payload
            doc_payload = {
                "key": doc_id,
                "title": lesson_note.get('lessonTitle', 'Untitled Lesson'),
                "url": f"{self.onlyoffice_url}/documents/{doc_id}",
                "fileType": "docx",
                "content": content
            }
            
            # Create document via OnlyOffice API
            response = requests.post(
                f"{self.onlyoffice_url}/api/documents/create",
                json=doc_payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "document_id": doc_id,
                    "document_url": f"{self.onlyoffice_url}/editor/{doc_id}",
                    "download_url": f"{self.onlyoffice_url}/documents/{doc_id}/download",
                    "title": lesson_note.get('lessonTitle', 'Untitled Lesson')
                }
            else:
                print(f"OnlyOffice API error: {response.status_code}")
                return {"success": False, "error": "OnlyOffice API failed"}
                
        except Exception as e:
            print(f"Error creating OnlyOffice document: {e}")
            return {"success": False, "error": str(e)}
    
    def store_lesson_info(self, lesson_data: Dict[str, Any]) -> bool:
        """Store lesson information in database"""
        try:
            # Create a document record for the lesson
            lesson_doc = Document(
                filename=f"{lesson_data.get('title', 'lesson')}.docx",
                content=lesson_data.get('content', ''),
                file_type='lesson_note',
                metadata={
                    'subject': lesson_data.get('subject'),
                    'class': lesson_data.get('class_level'),
                    'lesson_title': lesson_data.get('title'),
                    'document_id': lesson_data.get('document_id'),
                    'document_url': lesson_data.get('document_url'),
                    'status': 'generated',
                    'type': 'lesson_note'
                }
            )
            
            db.session.add(lesson_doc)
            db.session.commit()
            
            return True
            
        except Exception as e:
            print(f"Error storing lesson info: {e}")
            db.session.rollback()
            return False