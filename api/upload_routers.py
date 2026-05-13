import shutil
from datetime import datetime

import os
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from ingest.document_registry import list_documents, upsert_document, remove_document
from model.config import Settings as settings
from tools import reload_knowledge_base


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

    reload_knowledge_base()
    return {"message": "Upload successful", "filename": file.filename}


@router.get("/list")
async def list_file():
    documents = list_documents()
    return {
        "documents":documents,
    }

@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    document = get_document(filename)
    if not document:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = Path(document["file_path"])
    if file_path.exists():
        file_path.unlink()
    
    remove_document(filename)
    reload_knowledge_base()
    return {"message": "Deleted successfully", "filename": filename}

def get_document(filename: str):
    from ingest.document_registry import get_document as get_doc
    return get_doc(filename)
