from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.schemas import SearchRequest, SearchResponse, AskRequest, AskResponse
from app.services.retrieval import search_chunks
from app.services.rag import synthesize_answer

router = APIRouter(tags=["search"])


@router.post("/search", response_model=SearchResponse, dependencies=[Depends(verify_api_key)])
def search(payload: SearchRequest, db: Session = Depends(get_db)):
    results = search_chunks(db, payload.query, payload.top_k)
    return SearchResponse(results=results)


@router.post("/ask", response_model=AskResponse, dependencies=[Depends(verify_api_key)])
def ask(payload: AskRequest, db: Session = Depends(get_db)):
    chunks = search_chunks(db, payload.query, payload.top_k)
    answer, mode = synthesize_answer(payload.query, chunks)
    return AskResponse(answer=answer, sources=chunks, mode=mode)
