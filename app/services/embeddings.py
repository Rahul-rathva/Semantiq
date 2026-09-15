"""
Local embedding generation — no external API key required.
Uses sentence-transformers so the whole pipeline runs offline/free,
which matters for a demo project reviewers will actually spin up.
"""
from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer

from app.config import settings


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(settings.embedding_model)


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()


def embed_text(text: str) -> List[float]:
    return embed_texts([text])[0]
