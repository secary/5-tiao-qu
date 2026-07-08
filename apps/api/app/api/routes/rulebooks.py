from uuid import uuid4

from fastapi import APIRouter, File, UploadFile, status

from app.domain.schemas import RulebookSummary, RulebookUploadResponse

router = APIRouter()


@router.get("", response_model=list[RulebookSummary])
async def list_rulebooks() -> list[RulebookSummary]:
    return []


@router.post(
    "/upload",
    response_model=RulebookUploadResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_rulebook(file: UploadFile = File(...)) -> RulebookUploadResponse:
    rulebook_id = uuid4()
    return RulebookUploadResponse(
        rulebook_id=rulebook_id,
        file_name=file.filename or "rulebook.pdf",
        import_status="uploaded",
        message="上传入口已就绪，文件持久化和导入任务将在 P1 接入。",
    )
