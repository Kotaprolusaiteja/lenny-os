import httpx
from typing import List, Dict, Any
from backend.app.config import settings
from backend.app.llm.provider import LLMProvider
from backend.app.core.errors import AppError, ErrorCode

class OllamaProvider(LLMProvider):
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        
    async def generate(self, messages: List[Dict[str, Any]], system_prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        async with httpx.AsyncClient(timeout=settings.ollama_timeout_seconds) as client:
            formatted_messages = [{"role": "system", "content": system_prompt}] + messages
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            try:
                response = await client.post(f"{self.base_url}/api/chat", json=payload)
                if response.status_code == 404:
                    raise AppError(ErrorCode.OLLAMA_MODEL_MISSING, f"Ollama model '{self.model}' not found.")
                response.raise_for_status()
                payload = response.json()
                content = payload.get("message", {}).get("content")
                if not isinstance(content, str):
                    raise AppError(ErrorCode.PROVIDER_ERROR, "Ollama returned an invalid response.")
                return content
            except httpx.ConnectError:
                raise AppError(ErrorCode.OLLAMA_UNAVAILABLE, "Could not connect to Ollama.")
            except httpx.TimeoutException:
                raise AppError(ErrorCode.OLLAMA_UNAVAILABLE, "Ollama connection timed out.")
            except AppError:
                raise
            except httpx.HTTPError as e:
                raise AppError(ErrorCode.OLLAMA_UNAVAILABLE, f"Ollama request failed: {e}")
            
    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False

    def provider_name(self) -> str:
        return "ollama"

    def model_name(self) -> str:
        return self.model
