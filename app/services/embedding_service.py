import numpy as np
from flask import current_app
import re
import os
import hashlib

# Safe import of sentence_transformers with fallback
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: sentence_transformers not available: {e}")
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False
except Exception as e:
    print(f"Warning: sentence_transformers import error: {e}")
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False

class EmbeddingService:
    """Service for creating and managing text embeddings"""
    
    def __init__(self):
        self.model = None
        self._use_fallback_embedding = False
        self._setup_environment()
        self._load_model()
    
    def _setup_environment(self):
        """Setup environment for offline/local model usage"""
        # Set HuggingFace to use local cache and increase timeouts
        os.environ['TRANSFORMERS_OFFLINE'] = '0'  # Allow downloads but with fallback
        os.environ['HF_HUB_OFFLINE'] = '0'
        os.environ['SENTENCE_TRANSFORMERS_HOME'] = os.path.join(os.getcwd(), 'models')
        
        # Create models directory if it doesn't exist
        models_dir = os.path.join(os.getcwd(), 'models')
        os.makedirs(models_dir, exist_ok=True)
    
    def _load_model(self):
        """Load the embedding model with enhanced error handling and caching"""
        # Check if sentence_transformers is available
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            print("⚠️ SentenceTransformers not available - using fallback embedding")
            self.model = None
            self._use_fallback_embedding = True
            return
            
        try:
            model_name = current_app.config.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
            
            print(f"Loading embedding model: {model_name}")
            
            # Try to load with extended timeout
            import socket
            original_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(30)  # 30 second timeout
            
            try:
                # Try to load the model with timeout
                self.model = SentenceTransformer(model_name)
                print(f"✅ Successfully loaded embedding model: {model_name}")
                self._use_fallback_embedding = False
                
            except Exception as model_error:
                print(f"⚠️ Primary model loading failed: {model_error}")
                print("🔄 Trying local cache...")
                
                # Try loading from local cache first
                try:
                    models_dir = os.path.join(os.getcwd(), 'models')
                    local_path = os.path.join(models_dir, model_name.replace('/', '_'))
                    
                    if os.path.exists(local_path):
                        print(f"📁 Loading from local cache: {local_path}")
                        self.model = SentenceTransformer(local_path)
                        print("✅ Loaded from local cache successfully")
                        self._use_fallback_embedding = False
                    else:
                        raise Exception("Local cache not found")
                        
                except Exception as cache_error:
                    print(f"⚠️ Local cache loading failed: {cache_error}")
                    print("🔧 Using basic fallback embedding system...")
                    
                    # Ultimate fallback - use simple hash-based embedding
                    self.model = None
                    self._use_fallback_embedding = True
                    print("✅ Fallback embedding system initialized")
            
            finally:
                socket.setdefaulttimeout(original_timeout)
                
        except Exception as e:
            print(f"❌ Critical embedding service error: {e}")
            self.model = None
            self._use_fallback_embedding = True
            print("✅ Using fallback embedding system")
    
    def _generate_fallback_embedding(self, text, dimension=384):
        """Generate a simple hash-based embedding as fallback"""
        try:
            # Clean text
            cleaned_text = self._preprocess_text(text)
            
            # Create multiple hash-based features
            features = []
            
            # Hash-based features
            for i in range(0, dimension, 32):
                hash_input = f"{cleaned_text}_{i}".encode('utf-8')
                hash_obj = hashlib.md5(hash_input)
                hash_bytes = hash_obj.digest()
                
                # Convert to normalized floats
                hash_floats = [((b - 128) / 128.0) for b in hash_bytes[:32]]
                features.extend(hash_floats)
            
            # Ensure we have exactly the right dimension
            features = features[:dimension]
            while len(features) < dimension:
                features.append(0.0)
            
            # Normalize the vector
            norm = np.linalg.norm(features)
            if norm > 0:
                features = [f / norm for f in features]
            
            return features
            
        except Exception as e:
            print(f"Fallback embedding generation failed: {e}")
            # Return zero vector as last resort
            return [0.0] * dimension
    
    def get_embedding(self, text):
        """Generate embedding for text with fallback support"""
        
        # Use fallback embedding if model failed to load
        if self._use_fallback_embedding or self.model is None:
            print("🔧 Using fallback embedding generation")
            return self._generate_fallback_embedding(text)
        
        try:
            # Clean and preprocess text
            cleaned_text = self._preprocess_text(text)
            
            # Generate embedding using the loaded model
            embedding = self.model.encode(cleaned_text)
            
            # Convert to list for JSON serialization and database storage
            return embedding.tolist()
            
        except Exception as e:
            print(f"⚠️ Model embedding failed: {e}")
            print("🔧 Falling back to simple embedding")
            
            # Fall back to simple embedding if model fails
            return self._generate_fallback_embedding(text)
    
    def get_embeddings_batch(self, texts):
        """Generate embeddings for multiple texts with fallback support"""
        
        # Use fallback embedding if model failed to load
        if self._use_fallback_embedding or self.model is None:
            print("🔧 Using fallback embedding generation for batch")
            return [self._generate_fallback_embedding(text) for text in texts]
        
        try:
            # Clean and preprocess texts
            cleaned_texts = [self._preprocess_text(text) for text in texts]
            
            # Generate embeddings in batch
            embeddings = self.model.encode(cleaned_texts)
            
            # Convert to list of lists
            return [emb.tolist() for emb in embeddings]
            
        except Exception as e:
            print(f"⚠️ Batch embedding failed: {e}")
            print("🔧 Falling back to simple embedding for batch")
            
            # Fall back to simple embedding if model fails
            return [self._generate_fallback_embedding(text) for text in texts]
            raise Exception(f"Batch embedding generation failed: {str(e)}")
    
    def _preprocess_text(self, text):
        """Clean and preprocess text before embedding"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-]', '', text)
        
        # Trim to reasonable length for embedding (most models have token limits)
        max_length = 500  # Approximate token limit
        if len(text) > max_length:
            text = text[:max_length]
        
        return text.strip()
    
    def create_chunks(self, text, chunk_size=None, overlap=None):
        """Split text into chunks for embedding"""
        
        if chunk_size is None:
            chunk_size = current_app.config.get('CHUNK_SIZE', 500)
        if overlap is None:
            overlap = current_app.config.get('CHUNK_OVERLAP', 50)
        
        if not text or len(text.strip()) == 0:
            return []
        
        chunks = []
        
        # Split by sentences first for better chunk boundaries
        sentences = self._split_into_sentences(text)
        
        current_chunk = ""
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence would exceed chunk size
            if current_length + sentence_length > chunk_size and current_chunk:
                # Save current chunk
                chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap
                if overlap > 0 and len(current_chunk) > overlap:
                    current_chunk = current_chunk[-overlap:] + " " + sentence
                    current_length = len(current_chunk)
                else:
                    current_chunk = sentence
                    current_length = sentence_length
            else:
                # Add sentence to current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
                current_length += sentence_length
        
        # Add the final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # Filter out extremely short chunks (reduced from 50 to 10 chars)
        # This allows more flexibility while still filtering meaningless fragments
        chunks = [chunk for chunk in chunks if len(chunk.strip()) > 10]
        
        # If no valid chunks created, create one from the original text
        if not chunks and text and len(text.strip()) > 0:
            chunks = [text.strip()[:chunk_size]]  # Take first chunk_size characters
        
        return chunks
    
    def _split_into_sentences(self, text):
        """Split text into sentences"""
        
        # Simple sentence splitting using regex
        # This could be improved with a proper NLP library like spaCy
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Clean up sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def calculate_similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between two embeddings"""
        
        try:
            # Convert to numpy arrays if they aren't already
            emb1 = np.array(embedding1)
            emb2 = np.array(embedding2)
            
            # Calculate cosine similarity
            dot_product = np.dot(emb1, emb2)
            norm1 = np.linalg.norm(emb1)
            norm2 = np.linalg.norm(emb2)
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            raise Exception(f"Similarity calculation failed: {str(e)}")
    
    def find_similar_chunks(self, query_embedding, chunk_embeddings, top_k=5):
        """Find most similar chunks to a query embedding"""
        
        try:
            similarities = []
            
            for i, chunk_embedding in enumerate(chunk_embeddings):
                similarity = self.calculate_similarity(query_embedding, chunk_embedding)
                similarities.append((i, similarity))
            
            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Return top k results
            return similarities[:top_k]
            
        except Exception as e:
            raise Exception(f"Similar chunks search failed: {str(e)}")
    
    def get_model_info(self):
        """Get information about the current embedding model"""
        if not self.model:
            return None
        
        return {
            'model_name': getattr(self.model, '_model_name', 'unknown'),
            'max_seq_length': getattr(self.model, 'max_seq_length', 'unknown'),
            'embedding_dimension': self.model.get_sentence_embedding_dimension()
        }