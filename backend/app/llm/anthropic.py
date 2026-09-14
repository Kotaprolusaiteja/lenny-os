from typing import List, Dict, Any
from anthropic import AsyncAnthropic, APIError, APIConnectionError, APITimeoutError
from backend.app.config import settings
from backend.app.llm.provider import LLMProvider
from backend.app.llm.ollama import OllamaProvider
from backend.app.core.errors import AppError, ErrorCode

class AnthropicProvider(LLMProvider):
    def __init__(self):
        if not settings.anthropic_api_key:
            raise AppError(ErrorCode.ANTHROPIC_MISSING_KEY, "Anthropic API key is not configured.")
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        self.model = settings.anthropic_model

    async def generate(self, messages: List[Dict[str, Any]], system_prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        try:
            response = await self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            text_blocks = [block.text for block in response.content if getattr(block, "type", None) == "text"]
            if not text_blocks:
                raise AppError(ErrorCode.PROVIDER_ERROR, "Anthropic returned no text content.")
            return "".join(text_blocks)
        except APITimeoutError:
            raise AppError(ErrorCode.ANTHROPIC_TIMEOUT, "Anthropic API timed out.")
        except APIConnectionError:
            raise AppError(ErrorCode.PROVIDER_ERROR, "Anthropic API connection error.")
        except APIError as e:
            raise AppError(ErrorCode.PROVIDER_ERROR, f"Anthropic API error: {str(e)}")

    async def health_check(self) -> bool:
        return bool(settings.anthropic_api_key)

    def provider_name(self) -> str:
        return "anthropic"

    def model_name(self) -> str:
        return self.model

def get_llm_provider() -> LLMProvider:
    if settings.llm_provider.lower() == "anthropic":
        return AnthropicProvider()
    return OllamaProvider()
