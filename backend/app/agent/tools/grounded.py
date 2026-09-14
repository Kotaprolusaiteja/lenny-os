from typing import List, Dict, Any, Tuple
from backend.app.agent.execution import get_agent_executor
from backend.app.llm.provider import LLMProvider
from backend.app.rag.context import build_system_prompt, build_sources_response
from backend.app.schemas.api import SourceInfo

async def generate_grounded_answer(
    provider: LLMProvider,
    chunks: List[Dict[str, Any]],
    messages: List[Dict[str, Any]],
    prompt_type: str = "default",
    max_tokens: int = 1000,
) -> Tuple[str, List[SourceInfo]]:
    system_prompt = build_system_prompt(chunks, prompt_type)
    executor = get_agent_executor(provider)
    answer = await executor.generate(messages, system_prompt, max_tokens=max_tokens)
    sources = build_sources_response(chunks)
    return answer, sources
