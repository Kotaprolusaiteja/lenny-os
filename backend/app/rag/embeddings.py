from typing import List
import httpx
from backend.app.config import settings
from backend.app.core.errors import AppError, ErrorCode

_local_model = None
EMBEDDING_DIMENSION = 384

def validate_embedding(embedding: List[float]) -> List[float]:
    if len(embedding) != EMBEDDING_DIMENSION:
        raise AppError(
            ErrorCode.EMBEDDING_FAILURE,
            f"Embedding dimension {len(embedding)} does not match the configured vector({EMBEDDING_DIMENSION}) column.",
        )
    return embedding

def get_local_model():
    global _local_model
    if _local_model is None:
        from sentence_transformers import SentenceTransformer
        _local_model = SentenceTransformer(settings.embedding_model)
    return _local_model

async def generate_embedding_ollama(text: str) -> List[float]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{settings.ollama_base_url}/api/embeddings",
                json={"model": settings.ollama_embedding_model, "prompt": text}
            )
            response.raise_for_status()
            return validate_embedding(response.json()["embedding"])
        except Exception as e:
            raise AppError(ErrorCode.EMBEDDING_FAILURE, f"Ollama embedding failed: {str(e)}")

async def generate_embedding_openai(text: str) -> List[float]:
    if not settings.embedding_api_key:
        raise AppError(ErrorCode.EMBEDDING_FAILURE, "OpenAI embedding API key is not configured.")

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "https://api.openai.com/v1/embeddings",
                headers={"Authorization": f"Bearer {settings.embedding_api_key}"},
                json={
                    "input": text,
                    "model": settings.embedding_model,
                    "dimensions": EMBEDDING_DIMENSION,
                },
            )
            response.raise_for_status()
            return validate_embedding(response.json()["data"][0]["embedding"])
        except AppError:
            raise
        except Exception as e:
            raise AppError(ErrorCode.EMBEDDING_FAILURE, f"OpenAI embedding failed: {str(e)}")

async def generate_embedding(text: str) -> List[float]:
    if settings.embedding_provider == "openai":
        return await generate_embedding_openai(text)
    if settings.embedding_provider == "ollama":
        return await generate_embedding_ollama(text)
    
    # local
    model = get_local_model()
    return validate_embedding(model.encode(text).tolist())

async def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    if settings.embedding_provider == "openai":
        if not settings.embedding_api_key:
            raise AppError(ErrorCode.EMBEDDING_FAILURE, "OpenAI embedding API key is not configured.")

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    "https://api.openai.com/v1/embeddings",
                    headers={"Authorization": f"Bearer {settings.embedding_api_key}"},
                    json={
                        "input": texts,
                        "model": settings.embedding_model,
                        "dimensions": EMBEDDING_DIMENSION,
                    },
                )
                response.raise_for_status()
                data = response.json()["data"]
                ordered_embeddings = [item["embedding"] for item in sorted(data, key=lambda item: item["index"])]
                if len(ordered_embeddings) != len(texts):
                    raise AppError(
                        ErrorCode.EMBEDDING_FAILURE,
                        f"Expected {len(texts)} embeddings, got {len(ordered_embeddings)}",
                    )
                return [validate_embedding(embedding) for embedding in ordered_embeddings]
            except AppError:
                raise
            except Exception as e:
                raise AppError(ErrorCode.EMBEDDING_FAILURE, f"OpenAI embedding failed: {str(e)}")

    if settings.embedding_provider == "ollama":
        # Ollama API doesn't support batch, run sequentially or concurrently
        return [await generate_embedding_ollama(t) for t in texts]
    
    # local
    model = get_local_model()
    return [validate_embedding(embedding) for embedding in model.encode(texts).tolist()]
