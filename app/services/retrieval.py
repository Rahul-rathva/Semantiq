"""
Vector similarity search using pgvector's cosine distance operator (<=>).
"""
from typing import List

from sqlalchemy.orm import Session

from app.models import Chunk, Document
from app.services.embeddings import embed_text
from app.schemas import ChunkResult


def search_chunks(db: Session, query: str, top_k: int = 5) -> List[ChunkResult]:
    """
    Fetch the top_k nearest chunks by cosine distance and convert
    distance -> similarity score (1 = identical, 0 = unrelated).
    """
    query_vector = embed_text(query)

    rows = (
        db.query(
            Chunk,
            Document,
            Chunk.embedding.cosine_distance(query_vector).label("distance"),
        )
        .join(Document, Chunk.document_id == Document.id)
        .order_by("distance")
        .limit(top_k)
        .all()
    )

    return [
        ChunkResult(
            chunk_id=chunk.id,
            document_id=document.id,
            document_title=document.title,
            content=chunk.content,
            score=round(1 - float(distance), 4),
        )
        for chunk, document, distance in rows
    ]
