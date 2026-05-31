import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

os.environ["API_KEY"] = "test-key"
os.environ["AI_MODEL"] = "test-model"
os.environ["BASE_URL"] = "https://test.com/v1"
os.environ["AI_EMBEDDING_MODEL"] = "test-embedding"
os.environ["UPLOAD_DIR"] = str(ROOT_DIR / "tests" / "test_uploads")
os.environ["DATA_PATH"] = str(ROOT_DIR / "tests" / "test_data")


@pytest.fixture(autouse=True)
def clean_test_dirs():
    import shutil
    for d in [Path(os.environ["UPLOAD_DIR"]), Path(os.environ["DATA_PATH"])]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
    yield
    for d in [Path(os.environ["UPLOAD_DIR"]), Path(os.environ["DATA_PATH"])]:
        if d.exists():
            shutil.rmtree(d)


@pytest.fixture(autouse=True)
def mock_heavy_deps():
    with patch("api.upload_routers.reload_knowledge_base"):
        yield


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app) as c:
        yield c
