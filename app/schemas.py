import uuid
from typing import List, Optional

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    source: Optional[str] = None
    content: str


class DocumentOut(BaseModel):
    id: uuid.UUID
    title: str
    source: Optional[str]
    num_chunks: int

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class ChunkResult(BaseModel):
    chunk_id: uuid.UUID
    document_id: uuid.UUID
    document_title: str
    content: str
    score: float


class SearchResponse(BaseModel):
    results: List[ChunkResult]


class AskRequest(BaseModel):
    query: str
    top_k: int = 5


class AskResponse(BaseModel):
    answer: str
    sources: List[ChunkResult]
    mode: str  # "llm" or "extractive"
