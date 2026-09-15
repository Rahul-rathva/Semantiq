# SemantIQ — AI-Powered Semantic Search & RAG API

SemantIQ is a backend service that lets you ingest documents and query them
using natural language instead of exact keyword matching. It combines a
vector database, local embedding generation, and optional LLM-based answer
synthesis (Retrieval-Augmented Generation) behind a REST API.

Think of it as the backend for "ask questions about your own documents" —
the same pattern powering internal knowledge-base search, customer support
copilots, and developer-doc assistants at most product companies today.

## Why this project

- **Vector search is now a standard backend skill.** Most companies shipping
  AI features need someone who can design the retrieval layer, not just call
  an LLM API.
- **Runs fully offline/free.** Embeddings are generated locally via
  `sentence-transformers` — no API key required to ingest and search
  documents. An LLM key is optional, only needed for the `/ask` endpoint's
  generated answers.
- **Production shape, not a notebook.** Dockerized, has a CI pipeline,
  environment-based config, and a clean service-layer architecture —
  structured the way a real backend team organizes an API.

## Architecture

```
Client
  │
  ▼
FastAPI (app/main.py)
  │
  ├── /documents  → ingestion.py → chunk_text() → embeddings.py (sentence-transformers)
  │                                                     │
  │                                                     ▼
  │                                          PostgreSQL + pgvector (models.py)
  │
  └── /search, /ask → retrieval.py (cosine similarity via pgvector)
                             │
                             ▼
                        rag.py → Claude API (optional) or extractive fallback
```

## Tech stack

| Layer          | Choice                                   |
|----------------|-------------------------------------------|
| API            | FastAPI                                   |
| Database       | PostgreSQL + `pgvector` extension         |
| Embeddings     | `sentence-transformers` (all-MiniLM-L6-v2)|
| Caching        | Redis                                     |
| LLM (optional) | Anthropic Claude API                      |
| Auth           | API key (JWT helpers included for upgrade)|
| Infra          | Docker, Docker Compose                    |
| CI             | GitHub Actions (lint + test against real Postgres service) |

## Getting started

### 1. Clone and configure
```bash
git clone <your-repo-url>
cd semantiq
cp .env.example .env
```

### 2. Run with Docker Compose
```bash
docker compose up --build
```
The API will be available at `http://localhost:8000`. Interactive docs at
`http://localhost:8000/docs`.

### 3. Try it out
```bash
# Ingest a document
curl -X POST http://localhost:8000/documents \
  -H "x-api-key: semantiq-dev-key" \
  -H "Content-Type: application/json" \
  -d '{"title": "Onboarding Guide", "source": "internal", "content": "Your onboarding text here..."}'

# Semantic search
curl -X POST http://localhost:8000/search \
  -H "x-api-key: semantiq-dev-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "how do I set up my laptop", "top_k": 3}'

# Ask a question (RAG)
curl -X POST http://localhost:8000/ask \
  -H "x-api-key: semantiq-dev-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "how do I set up my laptop"}'
```

## Roadmap / good next additions (for your resume story)
- [ ] Swap fixed-size chunking for a recursive/semantic chunker
- [ ] Add hybrid search (BM25 + vector) for better recall
- [ ] Add Redis caching on repeated queries
- [ ] Replace API-key auth with full JWT user accounts
- [ ] Add reranking step (cross-encoder) before answer synthesis
- [ ] Load test with `locust` and document throughput numbers

## License
MIT
