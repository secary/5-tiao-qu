from uuid import uuid4

from fastapi import APIRouter

from app.domain.schemas import Answer, QuestionRequest, QuestionResponse

router = APIRouter()


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(payload: QuestionRequest) -> QuestionResponse:
    question_id = uuid4()
    answer = Answer(
        id=uuid4(),
        answer_type="not_found",
        conclusion="规则书中未找到明确说明。",
        explanation="检索和 LLM 供应商尚未接入，因此当前接口不会生成无引用裁定。",
        confidence=0.0,
        citations=[],
    )
    return QuestionResponse(question_id=question_id, answer=answer)
