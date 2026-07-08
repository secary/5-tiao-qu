from typing import Protocol
from uuid import UUID

from app.domain.schemas import Answer, Citation


class OcrProvider(Protocol):
    async def extract_pages(self, source_file: str) -> list[str]:
        """Return page-level text while preserving the original page order."""
        ...


class EmbeddingProvider(Protocol):
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector per input text."""
        ...


class VectorSearch(Protocol):
    async def search_rule_chunks(
        self,
        *,
        rulebook_id: UUID,
        query_embedding: list[float],
        limit: int,
    ) -> list[Citation]:
        """Return traceable rule chunks with page and source metadata."""
        ...


class LlmProvider(Protocol):
    async def answer_with_citations(
        self,
        *,
        question: str,
        citations: list[Citation],
    ) -> Answer:
        """Generate an answer using only the supplied citations."""
        ...
