from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.dialects import postgresql

from backend.app.agent.router import detect_intent
from backend.app.agent.execution import ClaudeAgentExecutor, ProviderAgentExecutor, get_agent_executor
from backend.app.config import settings
from backend.app.llm.anthropic import AnthropicProvider, get_llm_provider
from backend.app.llm.ollama import OllamaProvider
from backend.app.rag.context import build_context
from backend.app.rag.retrieval import search_similar_chunks
from backend.app.schemas.api import ArtifactResponse, ChatRequest
from backend.app.services.chat import serialize_artifact
from scripts.ingest_transcripts import chunk_text, parse_markdown


def test_sample_transcript_frontmatter_and_content():
    parsed = parse_markdown("data/transcripts/ep42_onboarding_lauryn_isford.md")

    assert parsed["metadata"]["title"]
    assert parsed["metadata"]["guest"]
    assert parsed["content"]


def test_chunking_preserves_overlap():
    chunks = chunk_text(" ".join(f"word{i}" for i in range(10)), chunk_size=4, overlap=1)

    assert chunks == [
        "word0 word1 word2 word3",
        "word3 word4 word5 word6",
        "word6 word7 word8 word9",
    ]


def test_provider_selection(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "ollama")
    assert isinstance(get_llm_provider(), OllamaProvider)

    monkeypatch.setattr(settings, "llm_provider", "anthropic")
    monkeypatch.setattr(settings, "anthropic_api_key", "test-key")
    assert isinstance(get_llm_provider(), AnthropicProvider)


def test_agent_executor_selection(monkeypatch):
    monkeypatch.setattr(settings, "anthropic_api_key", "test-key")

    assert isinstance(get_agent_executor(OllamaProvider()), ProviderAgentExecutor)
    assert isinstance(get_agent_executor(AnthropicProvider()), ClaudeAgentExecutor)


def test_anthropic_provider_requires_key(monkeypatch):
    monkeypatch.setattr(settings, "anthropic_api_key", None)

    with pytest.raises(Exception, match="API key"):
        AnthropicProvider()


def test_api_contract_requires_message():
    request = ChatRequest(session_id="session", message="What matters?")

    assert request.message == "What matters?"
    with pytest.raises(ValueError):
        ChatRequest(session_id="session", content="wrong field")


def test_retrieval_builds_cosine_ordered_query(monkeypatch):
    captured = {}

    async def fake_embedding(query):
        captured["query"] = query
        return [0.1] * 384

    class FakeResult:
        def all(self):
            return []

    class FakeSession:
        async def execute(self, statement):
            captured["statement"] = statement
            return FakeResult()

    monkeypatch.setattr("backend.app.rag.retrieval.generate_embedding", fake_embedding)
    import asyncio
    result = asyncio.run(search_similar_chunks(FakeSession(), "onboarding", 3))
    sql = str(captured["statement"].compile(dialect=postgresql.dialect()))

    assert result == []
    assert captured["query"] == "onboarding"
    assert "ORDER BY transcript_chunks.embedding <=>" in sql
    assert "LIMIT" in sql


def test_retrieval_context_preserves_source_metadata():
    chunks = [{
        "content": "Talk to users before building.",
        "source": {"episode": "Onboarding", "guest": "Lauryn", "path": "ep42.md"},
    }]

    assert "Episode 'Onboarding'" in build_context(chunks)
    assert "Talk to users before building." in build_context(chunks)


def test_artifact_serialization_round_trips_api_schema():
    artifact = {
        "id": uuid4(),
        "type": "markdown",
        "title": "Draft",
        "content": "# Draft",
        "created_at": datetime.now(UTC),
    }

    stored = serialize_artifact(artifact)
    parsed = ArtifactResponse.model_validate(stored)

    assert stored["id"] == str(artifact["id"])
    assert parsed.id == artifact["id"]
    assert parsed.created_at == artifact["created_at"]


@pytest.mark.parametrize(
    ("message", "intent"),
    [
        ("Write an essay about growth", "ship30"),
        ("Create a document for this", "artifact"),
        ("Challenge this assumption", "challenge"),
        ("What should I do next?", "qa"),
    ],
)
def test_agent_intent_routing(message, intent):
    assert detect_intent(message) == intent
