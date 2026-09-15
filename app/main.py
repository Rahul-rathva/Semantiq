from fastapi import FastAPI

from app.database import Base, engine
from app.api import routes_documents, routes_search

# Auto-create tables on startup (fine for a demo project; use Alembic
# migrations if you take this further).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SemantIQ",
    description="AI-powered semantic search & RAG API over your documents.",
    version="0.1.0",
)

app.include_router(routes_documents.router)
app.include_router(routes_search.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
