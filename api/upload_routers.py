import shutil
from datetime import datetime

from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from ingest.document_registry import list_documents, upsert_document
from model.config import Settings as settings


router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in settings.ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Failed! Only allow Markdown to upload!"
        )

    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    target_path = settings.UPLOAD_DIR / (file.filename or "")

    with open(target_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

        upsert_document({
            "filename": file.filename,
            "file_path":str(target_path),
            "updated_at":datetime.now().isoformat(timespec="seconds"),
        })


@router.get("/list")
async def list_file():
    documents = list_documents()
    return {
        "documents":documents,
    }
