from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: List[Dict[str, Any]], system_prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass

    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def model_name(self) -> str:
        pass
