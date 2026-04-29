import json
from datetime import datetime
from pathlib import Path
from model.config import Settings as settings

REGISTRY_PATH = settings.DOCUMENTS_REGISTRY_PATH


def _load_registry() -> list[dict]:
    if not REGISTRY_PATH.exists():
        return []

    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _save_registry(documents: list[dict]) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(
        json.dumps(documents, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def list_documents() -> list[dict]:
    documents = _load_registry()
    return sorted(documents, key=lambda item: item.get("updated_at", ""), reverse=True)


def get_document(filename: str) -> dict | None:
    normalized_name = Path(filename).name
    for document in _load_registry():
        if document.get("filename") == normalized_name:
            return document
    return None


def upsert_document(document: dict) -> None:
    documents = _load_registry()
    filtered = [
        item for item in documents
        if item.get("filename") != document.get("filename")
    ]
    filtered.append(document)
    _save_registry(filtered)


def remove_document(filename: str) -> dict | None:
    normalized_name = Path(filename).name
    documents = _load_registry()
    removed = None
    kept = []

    for item in documents:
        if item.get("filename") == normalized_name and removed is None:
            removed = item
            continue
        kept.append(item)

    _save_registry(kept)
    return removed


def clear_documents() -> None:
    _save_registry([])