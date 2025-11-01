import requests
import json
from flask import current_app
from typing import Optional, Dict, Any, List

class LLMService:
    """Service for interacting with various LLM providers"""
    
    def __init__(self):
        self.provider = current_app.config.get('DEFAULT_LLM_PROVIDER', 'ollama')
        self.ollama_url = current_app.config.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.lm_studio_url = current_app.config.get('LM_STUDIO_BASE_URL', 'http://localhost:1234')
        self.openai_api_key = current_app.config.get('OPENAI_API_KEY')
    
    def generate_response(self, message: str, context: str = "", system_prompt: str = "") -> str:
        """Generate response using the configured LLM provider"""
        
        try:
            if self.provider == 'ollama':
                return self._ollama_generate(message, context, system_prompt)
            elif self.provider == 'lm_studio':
                return self._lm_studio_generate(message, context, system_prompt)
            elif self.provider == 'openai':
                return self._openai_generate(message, context, system_prompt)
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
                
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
    
    def _ollama_generate(self, message: str, context: str, system_prompt: str) -> str:
        """Generate response using Ollama"""
        
        # Build the prompt with context
        full_prompt = self._build_rag_prompt(message, context, system_prompt)
        
        payload = {
            "model": "deepseek-coder-v2:16b",  # Use the available model
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2000
            }
        }
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', 'No response generated')
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def _lm_studio_generate(self, message: str, context: str, system_prompt: str) -> str:
        """Generate response using LM Studio"""
        
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add context if provided
        if context:
            messages.append({
                "role": "system", 
                "content": f"Context information:\n{context}\n\nPlease answer the following question using the context provided when relevant."
            })
        
        # Add user message
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": "local-model",  # LM Studio default
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.lm_studio_url}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"LM Studio API error: {str(e)}")
    
    def _openai_generate(self, message: str, context: str, system_prompt: str) -> str:
        """Generate response using OpenAI API"""
        
        if not self.openai_api_key:
            raise Exception("OpenAI API key not configured")
        
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add context if provided
        if context:
            messages.append({
                "role": "system", 
                "content": f"Context information:\n{context}\n\nPlease answer the following question using the context provided when relevant."
            })
        
        # Add user message
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _build_rag_prompt(self, message: str, context: str, system_prompt: str) -> str:
        """Build a RAG prompt for single-prompt models like Ollama"""
        
        prompt_parts = []
        
        if system_prompt:
            prompt_parts.append(f"System: {system_prompt}")
        
        if context:
            prompt_parts.append(f"Context information:\n{context}")
            prompt_parts.append("Please answer the following question using the context provided when relevant.")
        
        prompt_parts.append(f"Human: {message}")
        prompt_parts.append("Assistant:")
        
        return "\n\n".join(prompt_parts)
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models for the current provider"""
        
        try:
            if self.provider == 'ollama':
                return self._get_ollama_models()
            elif self.provider == 'lm_studio':
                return self._get_lm_studio_models()
            elif self.provider == 'openai':
                return self._get_openai_models()
            else:
                return []
                
        except Exception as e:
            print(f"Failed to get models: {e}")
            return []
    
    def _get_ollama_models(self) -> List[Dict[str, Any]]:
        """Get available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return result.get('models', [])
            
        except Exception:
            return []
    
    def _get_lm_studio_models(self) -> List[Dict[str, Any]]:
        """Get available LM Studio models"""
        try:
            response = requests.get(f"{self.lm_studio_url}/v1/models", timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return result.get('data', [])
            
        except Exception:
            return []
    
    def _get_openai_models(self) -> List[Dict[str, Any]]:
        """Get available OpenAI models (predefined list)"""
        return [
            {"id": "gpt-3.5-turbo", "object": "model"},
            {"id": "gpt-4", "object": "model"},
            {"id": "gpt-4-turbo", "object": "model"}
        ]
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to the LLM provider"""
        
        try:
            if self.provider == 'ollama':
                response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
                response.raise_for_status()
                return {"status": "connected", "provider": "ollama"}
                
            elif self.provider == 'lm_studio':
                response = requests.get(f"{self.lm_studio_url}/v1/models", timeout=5)
                response.raise_for_status()
                return {"status": "connected", "provider": "lm_studio"}
                
            elif self.provider == 'openai':
                if not self.openai_api_key:
                    return {"status": "error", "message": "API key not configured"}
                
                headers = {"Authorization": f"Bearer {self.openai_api_key}"}
                response = requests.get("https://api.openai.com/v1/models", 
                                      headers=headers, timeout=5)
                response.raise_for_status()
                return {"status": "connected", "provider": "openai"}
                
            else:
                return {"status": "error", "message": f"Unknown provider: {self.provider}"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def switch_provider(self, provider: str) -> bool:
        """Switch to a different LLM provider"""
        
        valid_providers = ['ollama', 'lm_studio', 'openai']
        if provider not in valid_providers:
            return False
        
        self.provider = provider
        return True