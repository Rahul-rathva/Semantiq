"""
Chunking + ingestion pipeline.
Simple fixed-size sliding window chunker — swap for a semantic/recursive
chunker later if you want to show off more advanced text-splitting logic.
"""
from typing import List

from sqlalchemy.orm import Session

from app.models import Document, Chunk
from app.services.embeddings import embed_texts


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks or [text]


def ingest_document(db: Session, title: str, source: str, content: str) -> Document:
    document = Document(title=title, source=source)
    db.add(document)
    db.flush()  # get document.id before creating chunks

    pieces = chunk_text(content)
    vectors = embed_texts(pieces)

    for idx, (piece, vector) in enumerate(zip(pieces, vectors)):
        db.add(
            Chunk(
                document_id=document.id,
                chunk_index=idx,
                content=piece,
                embedding=vector,
            )
        )

    db.commit()
    db.refresh(document)
    return document
