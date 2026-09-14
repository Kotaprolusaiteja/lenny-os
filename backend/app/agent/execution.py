from typing import Any, Dict, List, Protocol

from backend.app.llm.anthropic import AnthropicProvider
from backend.app.llm.provider import LLMProvider


class AgentExecutor(Protocol):
    async def generate(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
        max_tokens: int,
    ) -> str:
        ...


class ClaudeAgentExecutor:
    """Explicit execution boundary for Claude-backed agent skills."""

    def __init__(self, provider: AnthropicProvider):
        self.provider = provider

    async def generate(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
        max_tokens: int,
    ) -> str:
        return await self.provider.generate(
            messages,
            system_prompt,
            max_tokens=max_tokens,
        )


class ProviderAgentExecutor:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def generate(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
        max_tokens: int,
    ) -> str:
        return await self.provider.generate(
            messages,
            system_prompt,
            max_tokens=max_tokens,
        )


def get_agent_executor(provider: LLMProvider) -> AgentExecutor:
    if isinstance(provider, AnthropicProvider):
        return ClaudeAgentExecutor(provider)
    return ProviderAgentExecutor(provider)