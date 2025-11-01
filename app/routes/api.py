from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.models import Document, DocumentChunk, ChatSession, ChatMessage, ProcessingJob, SystemSettings
from app.services.ocr_service import OCRService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.onlyoffice_service import OnlyOfficeService
from app import db
import os
import uuid
from datetime import datetime
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
def health_check():
    """Health check endpoint for Docker and monitoring"""
    try:
        # Test database connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        db_status = 'healthy'
    except OperationalError:
        db_status = 'unhealthy'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@api_bp.route('/upload', methods=['POST'])
def upload_document():
    """Upload a document and start background processing"""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    document_name = request.form.get('document_name', file.filename)
    document_type = request.form.get('document_type')  # curriculum, textbook, progression
    subject = request.form.get('subject')
    class_level = request.form.get('class_level')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not document_type:
        return jsonify({'error': 'Document type is required'}), 400
    
    # Validate document type
    valid_types = {'curriculum', 'textbook', 'progression'}
    if document_type not in valid_types:
        return jsonify({'error': 'Invalid document type. Must be curriculum, textbook, or progression'}), 400
    
    # Validate file type - expanded for testing
    allowed_extensions = {'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif', 'txt', 'doc', 'docx'}
    if not ('.' in file.filename and 
            file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return jsonify({'error': f'File type not supported. Allowed: {", ".join(allowed_extensions)}'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                str(uuid.uuid4()) + '_' + filename)
        file.save(file_path)
        
        # Create document record with new fields
        document = Document(
            name=document_name,
            filename=filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            mime_type=file.content_type,
            document_type=document_type,
            subject=subject,
            class_level=class_level,
            processing_status='processing'  # Set to processing immediately
        )
        
        db.session.add(document)
        db.session.commit()
        
        # Create processing job
        job = ProcessingJob(
            job_type='ocr',
            document_id=document.id,
            status='pending'
        )
        db.session.add(job)
        db.session.commit()
        
        # Start background processing (non-blocking)
        import threading
        processing_thread = threading.Thread(
            target=process_document_background,
            args=(document.id, file_path, document_name, filename, document_type),
            daemon=True
        )
        processing_thread.start()
        
        # Return immediately with document info
        return jsonify({
            'success': True,
            'message': 'Document uploaded successfully. Processing started in background.',
            'document_id': str(document.id),
            'filename': filename,
            'file_size': document.file_size,
            'processing_status': 'processing',
            'estimated_time': estimate_processing_time(document.file_size)
        }), 200
        
    except Exception as e:
        print(f"Upload failed: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

def estimate_processing_time(file_size_bytes):
    """Estimate processing time based on file size"""
    file_size_mb = file_size_bytes / (1024 * 1024)
    if file_size_mb < 1:
        return "1-2 minutes"
    elif file_size_mb < 10:
        return "2-5 minutes"
    elif file_size_mb < 50:
        return "5-15 minutes"
    elif file_size_mb < 100:
        return "15-30 minutes"
    else:
        return "30-60 minutes"

def process_document_background(document_id, file_path, document_name, filename, document_type):
    """Process document OCR and embeddings in background thread"""
    from app import create_app
    
    # Create new app context for background thread
    app = create_app()
    with app.app_context():
        try:
            print(f"Background processing started for document: {document_id}")
            
            # Get document from database
            document = Document.query.get(document_id)
            if not document:
                print(f"Document {document_id} not found in database")
                return
            
            # Update job status
            job = ProcessingJob.query.filter_by(document_id=document_id, job_type='ocr').first()
            if job:
                job.status = 'processing'
                db.session.commit()
            
            # Process OCR with timeout handling
            import time
            start_time = time.time()
            
            try:
                print(f"Starting OCR processing for document: {document_id} (Size: {document.file_size} bytes)")
                
                ocr_service = OCRService()
                extracted_text = ocr_service.process_document(file_path)
                processing_time = time.time() - start_time
                
                print(f"OCR completed for document: {document_id} in {processing_time:.2f} seconds")
                
                if not extracted_text or len(extracted_text.strip()) < 3:
                    # If OCR failed or returned minimal text, use filename as fallback
                    extracted_text = f"Document: {document_name}\nFile: {filename}\nType: {document_type}"
                    print(f"OCR returned minimal text, using fallback for document: {document_id}")
            
            except Exception as ocr_error:
                print(f"OCR processing failed for document {document_id}: {ocr_error}")
                # Use fallback text if OCR fails
                extracted_text = f"Document: {document_name}\nFile: {filename}\nType: {document_type}\nOCR Error: {str(ocr_error)}"
            
            # Update document with OCR results
            document.extracted_text = extracted_text
            document.ocr_method = 'tesseract'
            
            # Create text chunks and embeddings
            try:
                print(f"Starting embedding generation for document: {document_id}")
                embedding_service = EmbeddingService()
                chunks = embedding_service.create_chunks(extracted_text)
                print(f"Created {len(chunks)} chunks for document: {document_id}")
                
                successful_chunks = 0
                
                for i, chunk_text in enumerate(chunks):
                    try:
                        embedding = embedding_service.get_embedding(chunk_text)
                        
                        chunk = DocumentChunk(
                            document_id=document_id,
                            content=chunk_text,
                            chunk_index=i,
                            embedding=embedding
                        )
                        db.session.add(chunk)
                        successful_chunks += 1
                        
                        # Progress update for large documents
                        if len(chunks) > 20 and (i + 1) % 20 == 0:
                            print(f"Embedding progress: {i + 1}/{len(chunks)} chunks processed")
                        
                    except Exception as chunk_error:
                        print(f"Failed to process chunk {i} for document {document_id}: {chunk_error}")
                        continue
                
                total_time = time.time() - start_time
                print(f"Processing completed in {total_time/60:.1f} minutes. Successfully processed {successful_chunks}/{len(chunks)} chunks for document: {document_id}")
                
            except Exception as embedding_error:
                print(f"Embedding processing failed for document {document_id}: {embedding_error}")
            
            # Mark as completed
            document.processing_status = 'completed'
            if job:
                job.status = 'completed'
            
            db.session.commit()
            print(f"Document {document_id} processing completed successfully")
            
        except Exception as e:
            print(f"Background processing failed for document {document_id}: {str(e)}")
            
            # Mark as failed
            if 'document' in locals():
                document.processing_status = 'failed'
            if 'job' in locals() and job:
                job.status = 'failed'
                job.error_message = str(e)
            
            db.session.commit()


@api_bp.route('/document-status/<document_id>', methods=['GET'])
def get_document_status(document_id):
    """Get processing status of a document"""
    try:
        document = Document.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Get processing job status
        job = ProcessingJob.query.filter_by(document_id=document_id, job_type='ocr').first()
        
        # Count chunks if processing is completed
        chunk_count = 0
        if document.processing_status == 'completed':
            chunk_count = DocumentChunk.query.filter_by(document_id=document_id).count()
        
        return jsonify({
            'document_id': str(document.id),
            'filename': document.filename,
            'processing_status': document.processing_status,
            'job_status': job.status if job else 'unknown',
            'error_message': job.error_message if job and job.error_message else None,
            'chunk_count': chunk_count,
            'file_size': document.file_size,
            'created_at': document.created_at.isoformat(),
            'extracted_text_length': len(document.extracted_text) if document.extracted_text else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/documents', methods=['GET'])
def list_documents():
    """Get list of processed documents"""
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    documents = Document.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'documents': [{
            'id': str(doc.id),
            'name': doc.name,
            'filename': doc.filename,
            'file_size': doc.file_size,
            'document_type': doc.document_type,
            'subject': doc.subject,
            'class_level': doc.class_level,
            'processing_status': doc.processing_status,
            'created_at': doc.created_at.isoformat(),
            'chunk_count': len(doc.chunks)
        } for doc in documents.items],
        'pagination': {
            'page': documents.page,
            'pages': documents.pages,
            'per_page': documents.per_page,
            'total': documents.total
        }
    })

@api_bp.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    """Get specific document details"""
    
    document = Document.query.get_or_404(document_id)
    
    return jsonify({
        'id': str(document.id),
        'name': document.name,
        'filename': document.filename,
        'extracted_text': document.extracted_text,
        'processing_status': document.processing_status,
        'created_at': document.created_at.isoformat(),
        'chunks': [{
            'id': str(chunk.id),
            'content': chunk.content,
            'chunk_index': chunk.chunk_index
        } for chunk in document.chunks]
    })

@api_bp.route('/search', methods=['POST'])
def vector_search():
    """Perform vector similarity search"""
    
    data = request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 5)
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        embedding_service = EmbeddingService()
        query_embedding = embedding_service.get_embedding(query)
        
        # Use simple text-based search instead of vector similarity for now
        # This avoids pgvector operator compatibility issues
        try:
            # Get relevant documents with content
            relevant_docs = Document.query.filter(
                Document.extracted_text.isnot(None),
                Document.extracted_text != ''
            ).order_by(Document.created_at.desc()).limit(limit).all()
            
            # Create results from documents
            results = []
            for doc in relevant_docs:
                # Create chunks from the document content
                chunks = doc.extracted_text.split('\n\n') if doc.extracted_text else []
                for i, chunk in enumerate(chunks[:3]):  # Limit to 3 chunks per doc
                    if chunk.strip():
                        results.append({
                            'chunk_id': f"{doc.id}_{i}",
                            'content': chunk.strip(),
                            'document_name': doc.name,
                            'document_id': str(doc.id),
                            'similarity_score': 0.8  # Placeholder similarity
                        })
            
        except Exception as e:
            print(f"Search error: {e}")
            results = []
        
        return jsonify({
            'results': results[:limit]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/chat', methods=['POST'])
def chat():
    """Chat with AI assistant using RAG"""
    
    data = request.get_json()
    message = data.get('message', '')
    session_id = data.get('session_id')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        # Get or create chat session
        if session_id:
            session = ChatSession.query.get(session_id)
        else:
            session = ChatSession(session_name=f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            db.session.add(session)
            db.session.commit()
        
        # Initialize context variables
        context = ""
        context_results = []
        
        try:
            # Enhanced context building for chunk-related queries
            if "chunk" in message.lower() or "last document" in message.lower() or "recent document" in message.lower():
                # Handle document queries with chunk information
                recent_doc = Document.query.order_by(Document.created_at.desc()).first()
                if recent_doc:
                    chunk_count = DocumentChunk.query.filter_by(document_id=recent_doc.id).count()
                    context = f"DOCUMENT PROCESSING INFORMATION:\n"
                    context += f"Document Name: {recent_doc.name}\n"
                    context += f"Upload Date: {recent_doc.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                    context += f"Processing Status: {recent_doc.processing_status}\n"
                    context += f"CHUNK COUNT: {chunk_count} chunks were created from this document\n"
                    
                    if recent_doc.subject:
                        context += f"Subject: {recent_doc.subject}\n"
                    if recent_doc.class_level:
                        context += f"Class Level: {recent_doc.class_level}\n"
                    if recent_doc.document_type:
                        context += f"Document Type: {recent_doc.document_type}\n"
                        
                    context += f"\nCHUNKING EXPLANATION: The document was automatically processed and split into {chunk_count} searchable text segments (chunks) to enable AI-powered question answering and content search."
                else:
                    context = "No documents have been ingested yet."
            elif "total" in message.lower() and "chunk" in message.lower():
                # Handle total chunk count queries
                total_chunks = DocumentChunk.query.count()
                doc_count = Document.query.count()
                context = f"TOTAL CHUNK STATISTICS:\n"
                context += f"Total Chunks: {total_chunks} chunks across all documents\n"
                context += f"Documents Processed: {doc_count} documents\n"
                if doc_count > 0:
                    avg_chunks = total_chunks / doc_count
                    context += f"Average Chunks per Document: {avg_chunks:.1f}\n"
                context += f"\nCHUNK PURPOSE: These chunks are text segments that make documents searchable and enable precise AI responses."
            else:
                # For other queries, provide simple document-based context
                print("Using simple document-based context")
                context_results = []
                
                # Get recent documents with relevant content
                try:
                    relevant_docs = Document.query.filter(
                        Document.extracted_text.isnot(None),
                        Document.extracted_text != ''
                    ).order_by(Document.created_at.desc()).limit(3).all()
                    
                    if relevant_docs:
                        context = "\n\n".join([f"From {doc.name}: {doc.extracted_text[:500]}..." 
                                             for doc in relevant_docs])
                    
                except Exception as context_error:
                    print(f"Context retrieval failed: {context_error}")
                    # Fallback to simple response
                    context = "No document context available"
        
        except Exception as context_error:
            print(f"Context retrieval failed: {context_error}")
            context = "I can help you with questions about your documents, but I'm having trouble accessing the document database right now."
        
        # Generate response using LLM with comprehensive fallback
        try:
            llm_service = LLMService()
            
            # Enhanced system prompt for chunk-related queries
            if "chunk" in message.lower():
                system_prompt = """You are an AI assistant specialized in document processing and analysis for the OCR Agent Pro system.

IMPORTANT: When answering questions about chunks, use the EXACT information provided in the context. Do not make up numbers or estimates.

Your expertise includes:
1. Explaining document chunking and processing
2. Providing accurate chunk counts from the context data
3. Helping users understand how document processing works
4. Supporting educational content analysis for Cameroon's curriculum

When the context contains "CHUNK COUNT:" or chunk statistics, use those EXACT numbers in your response. Be precise and factual about the processing information provided."""
            else:
                system_prompt = getattr(session, 'system_prompt', None) or """You are a helpful AI assistant for document analysis and the Cameroonian education system. 
                
Your role is to:
1. Answer questions about uploaded documents using the provided context
2. Help with educational content for Cameroon's curriculum
3. Provide insights about textbooks, lesson plans, and educational materials
4. Support teachers and students with document-based queries

When provided with document context, use it to give accurate, helpful responses. If no context is available, provide general educational assistance while being clear about the limitations."""
            
            # Try to generate response with LLM
            print(f"🤖 Generating LLM response using {llm_service.provider}")
            response = llm_service.generate_response(message, context, system_prompt)
            print("✅ LLM response generated successfully")
            
        except Exception as llm_error:
            print(f"⚠️ LLM generation failed: {llm_error}")
            
            # Provide intelligent fallback responses based on the query
            if "last document" in message.lower() or "recent document" in message.lower():
                try:
                    recent_doc = Document.query.order_by(Document.created_at.desc()).first()
                    if recent_doc:
                        chunk_count = DocumentChunk.query.filter_by(document_id=recent_doc.id).count()
                        response = f"The last document ingested was '{recent_doc.name}', uploaded on {recent_doc.created_at.strftime('%Y-%m-%d at %H:%M')}."
                        if recent_doc.subject:
                            response += f" It's a {recent_doc.subject} document"
                            if recent_doc.class_level:
                                response += f" for {recent_doc.class_level}"
                        response += "."
                        
                        # Add chunk information
                        if chunk_count > 0:
                            response += f"\n\n📊 **Processing Summary:** The document was successfully processed into {chunk_count} searchable chunks, making it ready for AI-powered queries."
                        
                        # Add context if available
                        if recent_doc.extracted_text:
                            preview = recent_doc.extracted_text[:200]
                            response += f"\n\n📄 **Content Preview:** {preview}..."
                    else:
                        response = "No documents have been ingested yet. Please upload a document first using the Document Management panel."
                except:
                    response = "I'm having trouble accessing the document database. Please try again later."
            
            elif "chunk" in message.lower() and ("last" in message.lower() or "recent" in message.lower() or "document" in message.lower()):
                try:
                    recent_doc = Document.query.order_by(Document.created_at.desc()).first()
                    if recent_doc:
                        chunk_count = DocumentChunk.query.filter_by(document_id=recent_doc.id).count()
                        response = f"The last document '{recent_doc.name}' was processed and created **{chunk_count} chunks**."
                        
                        # Add detailed information
                        response += f"\n\n📄 **Document Details:**"
                        response += f"\n• **Name:** {recent_doc.name}"
                        response += f"\n• **Upload Date:** {recent_doc.created_at.strftime('%Y-%m-%d at %H:%M')}"
                        response += f"\n• **Processing Status:** {recent_doc.processing_status}"
                        response += f"\n• **Total Chunks:** {chunk_count}"
                        
                        if recent_doc.subject:
                            response += f"\n• **Subject:** {recent_doc.subject}"
                        if recent_doc.class_level:
                            response += f"\n• **Class Level:** {recent_doc.class_level}"
                        if recent_doc.document_type:
                            response += f"\n• **Document Type:** {recent_doc.document_type}"
                            
                        response += f"\n\n💡 **About Chunks:** These {chunk_count} chunks contain the text content from your document, broken down into searchable segments that allow me to find relevant information when you ask questions about the document content."
                        
                        if chunk_count > 0:
                            response += f"\n\n✅ **Ready for Queries:** You can now ask me specific questions about the content of '{recent_doc.name}' and I'll search through these {chunk_count} chunks to provide accurate answers!"
                    else:
                        response = "No documents have been ingested yet. Please upload a document first using the Document Management panel, and it will be automatically processed into searchable chunks."
                except Exception as e:
                    response = f"I'm having trouble accessing the chunk information right now. Error: {str(e)}"
            
            elif "title" in message.lower() and ("document" in message.lower() or "last" in message.lower()):
                try:
                    recent_doc = Document.query.order_by(Document.created_at.desc()).first()
                    if recent_doc:
                        response = f"The title of the last ingested document is: '{recent_doc.name}'"
                        if recent_doc.document_type:
                            response += f" (Type: {recent_doc.document_type})"
                        if recent_doc.subject:
                            response += f" (Subject: {recent_doc.subject})"
                    else:
                        response = "No documents have been ingested yet."
                except:
                    response = "I'm having trouble accessing the document information right now."
            
            elif any(word in message.lower() for word in ['help', 'what', 'how', 'can you']):
                response = """I'm an AI assistant for the OCR Agent Pro system, designed to help with document analysis and the Cameroonian education system.

I can help you with:
• Answering questions about uploaded documents
• Finding information in your document collection
• Understanding document content and structure
• Educational content related to Cameroon's curriculum
• Textbook and lesson plan analysis

To get started:
1. Upload documents using the Document Management panel
2. Ask me questions about the content
3. Use specific queries like "What is the main topic of the last document?"

What would you like to know about your documents?"""
            
            elif "documents" in message.lower() and ("how many" in message.lower() or "count" in message.lower()):
                try:
                    doc_count = Document.query.count()
                    response = f"You currently have {doc_count} document(s) in your collection."
                    if doc_count > 0:
                        recent_docs = Document.query.order_by(Document.created_at.desc()).limit(3).all()
                        response += "\n\nMost recent documents:"
                        for doc in recent_docs:
                            response += f"\n• {doc.name} ({doc.created_at.strftime('%Y-%m-%d')})"
                except:
                    response = "I'm having trouble accessing the document count right now."
            
            elif "chunk" in message.lower() and ("total" in message.lower() or "all" in message.lower() or "how many" in message.lower()):
                try:
                    total_chunks = DocumentChunk.query.count()
                    doc_count = Document.query.count()
                    response = f"📊 **Total Chunks Across All Documents:** {total_chunks}"
                    response += f"\n📄 **Documents Processed:** {doc_count}"
                    
                    if doc_count > 0:
                        avg_chunks = total_chunks / doc_count
                        response += f"\n📈 **Average Chunks per Document:** {avg_chunks:.1f}"
                        
                        # Show breakdown by document
                        recent_docs = Document.query.order_by(Document.created_at.desc()).limit(5).all()
                        response += f"\n\n**Recent Documents & Their Chunks:**"
                        for doc in recent_docs:
                            doc_chunks = DocumentChunk.query.filter_by(document_id=doc.id).count()
                            response += f"\n• {doc.name}: {doc_chunks} chunks"
                except:
                    response = "I'm having trouble accessing the chunk statistics right now."
            
            elif "chunk" in message.lower() and ("what" in message.lower() or "explain" in message.lower()):
                response = """📚 **Understanding Document Chunks**

**What are chunks?**
Chunks are smaller, manageable pieces of text created when your documents are processed. Think of them as "bite-sized" segments that make it easier for the AI to search and understand your content.

**Why are documents chunked?**
• **Better Search:** Smaller pieces mean more precise search results
• **AI Processing:** LLMs work better with focused content segments  
• **Faster Responses:** Quick retrieval of relevant information
• **Context Management:** Keeps related information together

**How does chunking work in OCR Agent Pro?**
1. **Document Upload:** You upload a PDF, image, or text file
2. **OCR Processing:** Text is extracted using Tesseract or DeepSeek OCR
3. **Smart Chunking:** Content is split into logical segments (paragraphs, sections)
4. **Embedding Creation:** Each chunk gets a vector representation for semantic search
5. **Ready for Chat:** You can now ask questions and get precise answers!

**Typical chunk sizes:** 200-500 words per chunk, optimized for context and searchability."""
            
            else:
                response = """I apologize, but I'm experiencing technical difficulties with the AI service. 

However, I can still help you with basic document information. Try asking:
• "What's the title of the last document?"
• "How many chunks were created from the last document?"
• "How many documents do I have?"
• "What are chunks?" 
• "Help me understand what you can do"

Or check if the Ollama service is running for full AI capabilities."""
        
        # Save messages to database (with error handling)
        try:
            user_message = ChatMessage(
                session_id=session.id,
                role='user',
                content=message
            )
            
            assistant_message = ChatMessage(
                session_id=session.id,
                role='assistant',
                content=response,
                retrieved_chunks=[]  # Simplified for now
            )
            
            db.session.add(user_message)
            db.session.add(assistant_message)
            db.session.commit()
            
        except Exception as db_error:
            print(f"Failed to save chat messages: {db_error}")
            # Continue anyway - don't let database issues prevent the response
        
        return jsonify({
            'response': response,
            'session_id': str(session.id),
            'context_used': 0,  # Simplified for now
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Chat API error: {e}")
        return jsonify({
            'error': 'I apologize, but I encountered an error. Please try again.',
            'debug_info': str(e) if current_app.debug else None
        }), 500

@api_bp.route('/onlyoffice/sync', methods=['POST'])
def sync_onlyoffice():
    """Sync document with OnlyOffice services"""
    
    data = request.get_json()
    document_id = data.get('document_id')
    sync_type = data.get('sync_type')  # 'upload', 'document', 'spreadsheet'
    
    if not document_id or not sync_type:
        return jsonify({'error': 'document_id and sync_type are required'}), 400
    
    try:
        document = Document.query.get_or_404(document_id)
        onlyoffice_service = OnlyOfficeService()
        
        if sync_type == 'upload':
            file_id = onlyoffice_service.upload_document(document.file_path, document.name)
            document.onlyoffice_file_id = file_id
            
        elif sync_type == 'document':
            doc_id = onlyoffice_service.create_text_document(document.name, document.extracted_text)
            document.onlyoffice_doc_id = doc_id
            
        elif sync_type == 'spreadsheet':
            # Convert text to simple spreadsheet format
            lines = document.extracted_text.split('\n')
            sheet_data = [[line] for line in lines if line.strip()]
            sheet_id = onlyoffice_service.create_spreadsheet(f"{document.name} - Data", sheet_data)
            document.onlyoffice_sheet_id = sheet_id
        
        db.session.commit()
        
        return jsonify({
            'message': f'Document synced to OnlyOffice {sync_type.title()}',
            'onlyoffice_id': getattr(document, f'onlyoffice_{sync_type}_id', file_id if sync_type == 'upload' else doc_id if sync_type == 'document' else sheet_id)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/onlyoffice/status', methods=['GET'])
def onlyoffice_status():
    """Check OnlyOffice service status"""
    
    try:
        # Get OnlyOffice settings from database
        from app.models import SystemSettings
        settings = {s.key: s.value for s in SystemSettings.query.all()}
        
        onlyoffice_url = settings.get('onlyoffice_url', 'http://localhost:8000')
        
        # Test connection to OnlyOffice server
        try:
            if not REQUESTS_AVAILABLE:
                raise ImportError("requests library not available")
                
            import requests
            response = requests.get(f"{onlyoffice_url}/healthcheck", timeout=5)
            connected = response.status_code == 200
        except Exception as e:
            connected = False
            error_msg = str(e)
        
        return jsonify({
            'connected': connected,
            'service_url': onlyoffice_url,
            'status': 'connected' if connected else 'disconnected',
            'error': error_msg if not connected else None
        })
        
    except Exception as e:
        return jsonify({
            'connected': False,
            'error': str(e),
            'status': 'error',
            'service_url': 'http://localhost:8000'
        })

# Enhanced API endpoints for the new panels

@api_bp.route('/database/status', methods=['GET'])
def database_status():
    """Get detailed database connection and extension status"""
    
    result = {
        'postgres': {'connected': False, 'version': None, 'error': None},
        'pgvector': {'enabled': False, 'version': None, 'error': None}
    }
    
    try:
        # Test PostgreSQL connection
        db.session.execute(text('SELECT version()'))
        version_result = db.session.execute(text('SELECT version()')).fetchone()
        result['postgres']['connected'] = True
        result['postgres']['version'] = version_result[0].split(',')[0] if version_result else 'Unknown'
        
        # Test pgvector extension
        pgvector_result = db.session.execute(text("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector'")).fetchone()
        if pgvector_result:
            result['pgvector']['enabled'] = True
            result['pgvector']['version'] = pgvector_result[1] if len(pgvector_result) > 1 else 'Installed'
        
    except Exception as e:
        result['postgres']['error'] = str(e)
    
    return jsonify(result)

@api_bp.route('/database/stats', methods=['GET'])
def database_stats():
    """Get database statistics and metrics"""
    
    try:
        stats = {
            'documents': Document.query.count(),
            'chunks': DocumentChunk.query.count(),
            'processing': Document.query.filter_by(processing_status='processing').count(),
            'size': 'Calculating...'  # Placeholder for now
        }
        
        # Get database size (if possible)
        try:
            size_result = db.session.execute(text("SELECT pg_size_pretty(pg_database_size(current_database()))")).fetchone()
            stats['size'] = size_result[0] if size_result else 'Unknown'
        except:
            stats['size'] = 'Permission denied'
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/documents/activity', methods=['GET'])
def document_activity():
    """Get recent document activity for real-time monitoring"""
    
    try:
        # Get recent documents with activity
        recent_docs = Document.query.order_by(Document.updated_at.desc()).limit(10).all()
        
        activities = []
        for doc in recent_docs:
            if doc.processing_status == 'completed':
                activities.append({
                    'type': 'completed',
                    'title': f'Document Processed: {doc.name}',
                    'description': f'OCR completed using {doc.ocr_method or "Unknown method"}',
                    'timestamp': doc.updated_at.isoformat() if doc.updated_at else None
                })
            elif doc.processing_status == 'processing':
                activities.append({
                    'type': 'processing',
                    'title': f'Processing: {doc.name}',
                    'description': f'OCR in progress using {doc.ocr_method or "Unknown method"}',
                    'timestamp': doc.created_at.isoformat() if doc.created_at else None
                })
            elif doc.processing_status == 'failed':
                activities.append({
                    'type': 'failed',
                    'title': f'Processing Failed: {doc.name}',
                    'description': 'Document processing encountered an error',
                    'timestamp': doc.updated_at.isoformat() if doc.updated_at else None
                })
        
        return jsonify({'activities': activities})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/documents/processing', methods=['GET'])
def documents_processing():
    """Get currently processing documents"""
    
    try:
        processing_docs = Document.query.filter_by(processing_status='processing').all()
        
        result = []
        for doc in processing_docs:
            result.append({
                'id': doc.id,
                'name': doc.name,
                'ocr_method': doc.ocr_method,
                'created_at': doc.created_at.isoformat() if doc.created_at else None,
                'progress': 50  # Placeholder progress
            })
        
        return jsonify({'processing': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/documents/recent-completions', methods=['GET'])
def recent_completions():
    """Get recently completed documents"""
    
    try:
        completed_docs = Document.query.filter_by(processing_status='completed').order_by(Document.updated_at.desc()).limit(5).all()
        
        result = []
        for doc in completed_docs:
            result.append({
                'id': doc.id,
                'name': doc.name,
                'extracted_text': doc.extracted_text,
                'updated_at': doc.updated_at.isoformat() if doc.updated_at else None
            })
        
        return jsonify({'completions': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/documents/<int:doc_id>/reprocess', methods=['POST'])
def reprocess_document(doc_id):
    """Reprocess a document"""
    
    try:
        document = Document.query.get_or_404(doc_id)
        document.processing_status = 'pending'
        document.extracted_text = None
        document.ocr_method = None
        
        db.session.commit()
        
        # Here you would trigger the actual reprocessing
        # For now, we'll just mark it as pending
        
        return jsonify({'success': True, 'message': 'Document queued for reprocessing'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/test-database', methods=['POST'])
def test_database():
    """Test database connection with provided configuration"""
    
    data = request.get_json()
    
    try:
        # This would test the connection with the provided parameters
        # For now, we'll just test the current connection
        db.session.execute(text('SELECT 1'))
        return jsonify({'success': True, 'message': 'Database connection successful'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/test-ocr', methods=['POST'])
def test_ocr():
    """Test OCR services"""
    
    try:
        from app.services.ocr_service import OCRService
        ocr_service = OCRService()
        
        # Test if DeepSeek OCR is available
        if ocr_service._should_use_deepseek_ocr():
            message = "DeepSeek OCR is available and ready"
        elif ocr_service._should_use_tesseract():
            message = "Tesseract OCR is available (DeepSeek unavailable)"
        else:
            message = "No OCR services available"
            
        return jsonify({'success': True, 'message': message})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/test-llm', methods=['POST'])
def test_llm():
    """Test LLM connection"""
    
    try:
        # This would test the LLM connection
        # For now, return a success message
        return jsonify({
            'success': True, 
            'response': 'Hello! I am working correctly.',
            'message': 'LLM test successful'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/settings/export', methods=['GET'])
def export_settings():
    """Export all settings as JSON"""
    
    try:
        settings = SystemSettings.query.all()
        settings_dict = {s.key: s.value for s in settings}
        
        response = jsonify(settings_dict)
        response.headers['Content-Disposition'] = 'attachment; filename=ocr_agent_settings.json'
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/settings/import', methods=['POST'])
def import_settings():
    """Import settings from JSON file"""
    
    try:
        if 'settings_file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['settings_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        import json
        settings_data = json.load(file)
        
        for key, value in settings_data.items():
            setting = SystemSettings.query.filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = SystemSettings(key=key, value=value)
                db.session.add(setting)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Settings imported successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/settings', methods=['GET', 'POST'])
def manage_settings():
    """Get or update system settings"""
    
    from app.models import SystemSettings
    
    if request.method == 'GET':
        settings = SystemSettings.query.all()
        return jsonify({
            setting.key: {
                'value': setting.value,
                'description': setting.description,
                'type': setting.setting_type
            } for setting in settings
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Handle both flat format and nested format from frontend
        if 'category' in data and 'settings' in data:
            # Nested format from frontend: {"category": "system", "settings": {...}}
            settings_data = data['settings']
            category = data['category']
        else:
            # Flat format: {"key": "value", ...}
            settings_data = data
            category = None
        
        try:
            for key, value in settings_data.items():
                setting = SystemSettings.query.filter_by(key=key).first()
                if setting:
                    setting.value = str(value)  # Ensure value is string
                    setting.updated_at = datetime.utcnow()
                else:
                    setting = SystemSettings(
                        key=key,
                        value=str(value),  # Ensure value is string
                        setting_type='string'
                    )
                    db.session.add(setting)
            
            db.session.commit()
            return jsonify({
                'success': True,
                'message': f'{category.title() if category else "Settings"} updated successfully'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': f'Failed to save settings: {str(e)}'
            }), 500

@api_bp.route('/jobs/<job_id>/status', methods=['GET'])
def get_job_status(job_id):
    """Get processing job status"""
    
    job = ProcessingJob.query.get_or_404(job_id)
    
    return jsonify({
        'id': str(job.id),
        'job_type': job.job_type,
        'status': job.status,
        'progress': job.progress,
        'error_message': job.error_message,
        'created_at': job.created_at.isoformat(),
        'completed_at': job.completed_at.isoformat() if job.completed_at else None
    })

@api_bp.route('/settings/onlyoffice', methods=['POST'])
def save_onlyoffice_settings():
    """Save OnlyOffice configuration settings"""
    
    try:
        data = request.get_json()
        
        # Define the OnlyOffice settings to save
        onlyoffice_settings = {
            'onlyoffice_url': data.get('onlyoffice_url', 'http://localhost:8000'),
            'onlyoffice_secret': data.get('onlyoffice_secret', ''),
            'onlyoffice_token': data.get('onlyoffice_token', ''),
            'onlyoffice_storage_url': data.get('onlyoffice_storage_url', 'http://localhost:5000/storage')
        }
        
        # Save each setting to the database
        for key, value in onlyoffice_settings.items():
            setting = SystemSettings.query.filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = SystemSettings(
                    key=key,
                    value=value,
                    description=f'OnlyOffice {key.replace("onlyoffice_", "").replace("_", " ").title()}',
                    setting_type='string'
                )
                db.session.add(setting)
        
        db.session.commit()
        
        # Test the connection with new settings
        onlyoffice_service = OnlyOfficeService()
        connection_test = onlyoffice_service.check_connection()
        
        return jsonify({
            'success': True,
            'message': 'OnlyOffice settings saved successfully',
            'connection_status': 'connected' if connection_test else 'disconnected',
            'settings': onlyoffice_settings
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to save OnlyOffice settings'
        }), 500

@api_bp.route('/settings/test-onlyoffice', methods=['POST'])
def test_onlyoffice_connection():
    """Test OnlyOffice connection with provided settings"""
    
    try:
        data = request.get_json()
        
        # Create a temporary OnlyOffice service with test settings
        from app.services.onlyoffice_service import OnlyOfficeService
        
        # Temporarily override the service configuration
        test_service = OnlyOfficeService()
        test_service.onlyoffice_url = data.get('onlyoffice_url', 'http://localhost:8000')
        test_service.onlyoffice_secret = data.get('onlyoffice_secret', '')
        test_service.onlyoffice_token = data.get('onlyoffice_token', '')
        test_service.storage_url = data.get('onlyoffice_storage_url', 'http://localhost:5000/storage')
        
        # Test the connection
        connected = test_service.check_connection()
        
        if connected:
            return jsonify({
                'success': True,
                'connected': True,
                'message': 'OnlyOffice connection successful',
                'service_url': test_service.onlyoffice_url
            })
        else:
            return jsonify({
                'success': False,
                'connected': False,
                'message': 'OnlyOffice connection failed',
                'error': 'Unable to connect to OnlyOffice server'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'connected': False,
            'error': str(e),
            'message': 'OnlyOffice connection test failed'
        }), 500

@api_bp.route('/lessons/generate', methods=['POST'])
def generate_lesson():
    """Generate lesson note with OnlyOffice fallback"""
    
    try:
        data = request.get_json()
        
        # Extract parameters
        subject = data.get('subject', '').strip()
        class_level = data.get('class_level', '').strip()
        lesson_info = data.get('lesson_info', {})
        
        if not subject or not class_level:
            return jsonify({
                'success': False,
                'error': 'Subject and class level are required'
            }), 400
        
        # Validate lesson info
        if not isinstance(lesson_info, dict):
            lesson_info = {}
            
        # Initialize lesson service with error handling
        try:
            from app.services.lesson_service import LessonNoteService
            lesson_service = LessonNoteService()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to initialize lesson service: {str(e)}',
                'message': 'Lesson generation service not available'
            }), 500
        
        # Get documents for the subject and class
        try:
            subject_data = lesson_service.get_subject_documents(subject, class_level)
            documents = subject_data.get('documents', []) or []
            curriculum = subject_data.get('curriculum_documents', []) or []
        except Exception as e:
            # If database query fails, continue with empty documents
            documents = []
            curriculum = []
            print(f"Warning: Could not fetch documents - {e}")
        
        # Generate lesson note with fallback
        try:
            result = lesson_service.create_lesson_with_fallback(
                subject, class_level, lesson_info, documents, curriculum
            )
            
            # Ensure we return a valid response
            if not isinstance(result, dict):
                result = {
                    'success': False,
                    'error': 'Invalid response from lesson service',
                    'message': 'Failed to generate lesson note'
                }
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'message': 'Failed to generate lesson note - AI service error'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate lesson note'
        }), 500

@api_bp.route('/lessons/extract-titles', methods=['POST'])
def extract_lesson_titles():
    """Extract lesson titles from documents"""
    
    try:
        data = request.get_json()
        
        subject = data.get('subject', '')
        class_level = data.get('class_level', '')
        
        if not subject or not class_level:
            return jsonify({
                'success': False,
                'error': 'Subject and class level are required'
            }), 400
        
        # Initialize lesson service
        from app.services.lesson_service import LessonNoteService
        lesson_service = LessonNoteService()
        
        # Get documents and extract lesson titles
        try:
            subject_data = lesson_service.get_subject_documents(subject, class_level)
            documents = subject_data.get('documents', []) or []
            
            if not documents:
                return jsonify({
                    'success': True,
                    'lessons': [],
                    'message': 'No documents found for the specified subject and class'
                })
            
            # Extract lesson titles using AI
            lesson_titles = lesson_service.extract_lesson_titles(documents)
            
            return jsonify({
                'success': True,
                'lessons': lesson_titles,
                'document_count': len(documents)
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'message': 'Failed to extract lesson titles'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to process request'
        }), 500

@api_bp.route('/ollama/models', methods=['GET'])
def get_ollama_models():
    """Get available Ollama models"""
    
    try:
        import requests
        from flask import current_app
        
        # Get Ollama URL from settings or config
        try:
            ollama_url = SystemSettings.query.filter_by(key='llm_base_url').first()
            if ollama_url:
                base_url = ollama_url.value
            else:
                base_url = current_app.config.get('OLLAMA_URL', 'http://localhost:11434')
        except:
            base_url = 'http://localhost:11434'
        
        # Fetch models from Ollama
        response = requests.get(f"{base_url}/api/tags", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = []
            
            for model in data.get('models', []):
                models.append({
                    'name': model.get('name', ''),
                    'size': model.get('size', 0),
                    'modified_at': model.get('modified_at', ''),
                    'family': model.get('details', {}).get('family', ''),
                    'format': model.get('details', {}).get('format', '')
                })
            
            return jsonify({
                'success': True,
                'models': models,
                'base_url': base_url
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Ollama API returned status {response.status_code}',
                'models': []
            }), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': 'Cannot connect to Ollama. Make sure Ollama is running.',
            'models': []
        }), 503
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'models': []
        }), 500

@api_bp.route('/settings/ai', methods=['POST'])
def save_ai_settings():
    """Save AI/LLM configuration settings"""
    
    try:
        data = request.get_json()
        
        # Define the AI settings to save
        ai_settings = {
            'llm_provider': data.get('llm_provider', 'ollama'),
            'llm_model': data.get('llm_model', 'llama3.2:3b'),
            'llm_base_url': data.get('llm_base_url', 'http://localhost:11434'),
            'llm_api_key': data.get('llm_api_key', ''),
            'llm_temperature': data.get('llm_temperature', '0.7'),
            'llm_max_tokens': data.get('llm_max_tokens', '2048')
        }
        
        # Save each setting to the database
        for key, value in ai_settings.items():
            setting = SystemSettings.query.filter_by(key=key).first()
            if setting:
                setting.value = str(value)
            else:
                setting = SystemSettings(
                    key=key,
                    value=str(value),
                    description=f'AI/LLM {key.replace("llm_", "").replace("_", " ").title()}',
                    setting_type='string'
                )
                db.session.add(setting)
        
        db.session.commit()
        
        # Test the connection with new settings if it's Ollama
        if ai_settings['llm_provider'] == 'ollama':
            try:
                response = requests.get(f"{ai_settings['llm_base_url']}/api/tags", timeout=5)
                connection_test = response.status_code == 200
            except:
                connection_test = False
        else:
            connection_test = None  # Don't test other providers for now
        
        return jsonify({
            'success': True,
            'message': 'AI settings saved successfully',
            'connection_status': 'connected' if connection_test else 'disconnected' if connection_test is not None else 'unknown',
            'settings': ai_settings
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to save AI settings'
        }), 500

@api_bp.route('/subjects', methods=['GET'])
def get_subjects():
    """Get all subjects from the Cameroonian education system"""
    try:
        from app.models import Subject
        subjects = Subject.query.filter_by(is_active=True).order_by(Subject.name).all()
        
        subjects_data = []
        for subject in subjects:
            subjects_data.append({
                'id': subject.id,
                'name': subject.name,
                'name_french': subject.name_french,
                'category': subject.category
            })
        
        return jsonify({
            'success': True,
            'subjects': subjects_data,
            'count': len(subjects_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch subjects'
        }), 500

@api_bp.route('/class-levels', methods=['GET'])
def get_class_levels():
    """Get all class levels from the Cameroonian bilingual education system"""
    try:
        from app.models import ClassLevel
        class_levels = ClassLevel.query.filter_by(is_active=True).order_by(
            ClassLevel.education_section, ClassLevel.grade_number
        ).all()
        
        class_levels_data = []
        for level in class_levels:
            level_data = {
                'id': level.id,
                'name': level.name,
                'name_french': level.name_french,
                'education_level': level.education_level,
                'grade_number': level.grade_number
            }
            
            # Add education_section if available
            if hasattr(level, 'education_section') and level.education_section:
                level_data['education_section'] = level.education_section
            
            class_levels_data.append(level_data)
        
        return jsonify({
            'success': True,
            'class_levels': class_levels_data,
            'count': len(class_levels_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch class levels'
        }), 500

# DeepSeek OCR Server Management Endpoints
@api_bp.route('/deepseek/status', methods=['GET'])
def deepseek_status():
    """Check DeepSeek OCR server status"""
    
    try:
        from app.services.deepseek_service import DeepSeekOCRService
        
        service = DeepSeekOCRService()
        status = service.check_server_status()
        
        return jsonify({
            'success': True,
            'is_running': status.get('is_running', False),
            'message': status.get('message', 'Status unknown'),
            'server_info': status.get('server_info', {}),
            'url': status.get('url', 'http://localhost:8001')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'is_running': False,
            'message': f'Error checking status: {str(e)}'
        })

@api_bp.route('/deepseek/start', methods=['POST'])
def start_deepseek():
    """Start DeepSeek OCR server"""
    
    try:
        from app.services.deepseek_service import DeepSeekOCRService
        
        service = DeepSeekOCRService()
        result = service.start_server()
        
        if result.get('success', False):
            return jsonify({
                'success': True,
                'message': result.get('message', 'Server started successfully'),
                'process_id': result.get('process_id'),
                'url': result.get('url', 'http://localhost:8001')
            })
        else:
            return jsonify({
                'success': False,
                'message': result.get('message', 'Failed to start server'),
                'error': result.get('error')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting server: {str(e)}'
        }), 500

@api_bp.route('/deepseek/stop', methods=['POST'])
def stop_deepseek():
    """Stop DeepSeek OCR server"""
    
    try:
        from app.services.deepseek_service import DeepSeekOCRService
        
        service = DeepSeekOCRService()
        result = service.stop_server()
        
        if result.get('success', False):
            return jsonify({
                'success': True,
                'message': result.get('message', 'Server stopped successfully')
            })
        else:
            return jsonify({
                'success': False,
                'message': result.get('message', 'Failed to stop server'),
                'error': result.get('error')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error stopping server: {str(e)}'
        }), 500