"""
RAG answer synthesis.
If ANTHROPIC_API_KEY is set, calls Claude to synthesize a grounded answer
from retrieved chunks. Otherwise falls back to a clean extractive answer
(top chunk content) so the project runs fully offline with zero API cost.
"""
from typing import List

from app.config import settings
from app.schemas import ChunkResult


def build_context(chunks: List[ChunkResult]) -> str:
    return "\n\n---\n\n".join(
        f"[Source: {c.document_title}]\n{c.content}" for c in chunks
    )


def synthesize_answer(query: str, chunks: List[ChunkResult]) -> tuple[str, str]:
    if not chunks:
        return "No relevant documents found.", "extractive"

    if settings.anthropic_api_key:
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
            context = build_context(chunks)
            prompt = (
                f"Answer the question using ONLY the context below. "
                f"If the answer isn't in the context, say so.\n\n"
                f"Context:\n{context}\n\nQuestion: {query}"
            )
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            answer = "".join(
                block.text for block in response.content if block.type == "text"
            )
            return answer, "llm"
        except Exception as exc:  # noqa: BLE001
            # Fall through to extractive mode if the LLM call fails for any reason
            return f"(LLM call failed, showing top match instead: {exc})\n\n{chunks[0].content}", "extractive"

    return chunks[0].content, "extractive"
