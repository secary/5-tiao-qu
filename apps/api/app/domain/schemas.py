from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class ImportStatus(StrEnum):
    uploaded = "uploaded"
    extracting = "extracting"
    chunking = "chunking"
    embedding = "embedding"
    ready = "ready"
    failed = "failed"


class AnswerType(StrEnum):
    direct_rule = "direct_rule"
    related_inference = "related_inference"
    not_found = "not_found"
    conflict = "conflict"


class SourceType(StrEnum):
    base_rulebook = "base_rulebook"
    expansion_rulebook = "expansion_rulebook"
    faq = "faq"
    errata = "errata"
    player_note = "player_note"


class HealthResponse(BaseModel):
    status: str
    service: str


class BoundingBox(BaseModel):
    page_number: int
    x: float
    y: float
    width: float
    height: float


class Citation(BaseModel):
    id: UUID
    chunk_id: UUID
    page_number: int
    chapter_title: str | None = None
    chunk_text: str
    source_file: str
    source_type: SourceType = SourceType.base_rulebook
    source_priority: int = 100
    bounding_box: BoundingBox | None = None
    similarity_score: float | None = None


class Answer(BaseModel):
    id: UUID
    answer_type: AnswerType
    conclusion: str
    explanation: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    citations: list[Citation]


class QuestionRequest(BaseModel):
    rulebook_id: UUID
    question: str = Field(min_length=1)
    conversation_id: UUID | None = None


class QuestionResponse(BaseModel):
    question_id: UUID
    answer: Answer


class RulebookSummary(BaseModel):
    id: UUID
    board_game_id: UUID | None = None
    title: str
    version: str | None = None
    source_file: str
    import_status: ImportStatus


class RulebookUploadResponse(BaseModel):
    rulebook_id: UUID
    file_name: str
    import_status: ImportStatus
    message: str
