from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.database import get_db
from app.models import Document
from app.schemas import DocumentCreate, DocumentOut
from app.services.ingestion import ingest_document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentOut, dependencies=[Depends(verify_api_key)])
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    document = ingest_document(db, payload.title, payload.source, payload.content)
    return DocumentOut(
        id=document.id,
        title=document.title,
        source=document.source,
        num_chunks=len(document.chunks),
    )


@router.get("", response_model=list[DocumentOut], dependencies=[Depends(verify_api_key)])
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return [
        DocumentOut(
            id=d.id, title=d.title, source=d.source, num_chunks=len(d.chunks)
        )
        for d in documents
    ]
