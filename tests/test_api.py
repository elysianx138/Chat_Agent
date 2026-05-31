from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path


class TestRootEndpoint:

    def test_get_root_returns_html(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]


class TestChatEndpoint:

    @patch("api.chat_routers.create_agent")
    def test_chat_success(self, mock_create_agent, client):
        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock(return_value={
            "messages": [MagicMock(content="Hello! How can I help?")]
        })
        mock_create_agent.return_value = mock_agent

        resp = client.post("/chat", json={
            "query": "hello",
            "session_id": "test-1"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "answer" in data
        assert data["session_id"] == "test-1"

    @patch("api.chat_routers.create_agent")
    def test_chat_empty_query_rejected(self, mock_create_agent, client):
        resp = client.post("/chat", json={"query": ""})
        assert resp.status_code == 422

    @patch("api.chat_routers.create_agent")
    def test_chat_attribute_error_returns_502(self, mock_create_agent, client):
        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock(side_effect=AttributeError("bad attr"))
        mock_create_agent.return_value = mock_agent

        resp = client.post("/chat", json={"query": "hello"})
        assert resp.status_code == 502
        assert "API" in resp.json()["detail"]

    @patch("api.chat_routers.create_agent")
    def test_chat_generic_error_returns_500(self, mock_create_agent, client):
        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock(side_effect=ValueError("something broke"))
        mock_create_agent.return_value = mock_agent

        resp = client.post("/chat", json={"query": "hello"})
        assert resp.status_code == 500
        assert "Chat execution failed" in resp.json()["detail"]


class TestUploadEndpoint:

    def test_upload_markdown_success(self, client):
        resp = client.post(
            "/upload",
            files={"file": ("test.md", b"# Hello World", "text/markdown")}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "Upload successful"
        assert data["filename"] == "test.md"

    def test_upload_non_markdown_rejected(self, client):
        resp = client.post(
            "/upload",
            files={"file": ("test.txt", b"hello", "text/plain")}
        )
        assert resp.status_code == 400
        assert "Markdown" in resp.json()["detail"]

    def test_upload_file_persisted_to_disk(self, client):
        client.post(
            "/upload",
            files={"file": ("persist.md", b"# persist", "text/markdown")}
        )
        upload_path = Path(__file__).resolve().parent.parent / "tests" / "test_uploads" / "persist.md"
        assert upload_path.exists()
        assert upload_path.read_text() == "# persist"


class TestListEndpoint:

    def test_list_empty_when_no_uploads(self, client):
        resp = client.get("/list")
        assert resp.status_code == 200
        assert resp.json()["documents"] == []

    def test_list_returns_uploaded_file(self, client):
        client.post("/upload", files={"file": ("doc.md", b"# doc", "text/markdown")})
        resp = client.get("/list")
        assert resp.status_code == 200
        filenames = [d["filename"] for d in resp.json()["documents"]]
        assert "doc.md" in filenames


class TestDeleteEndpoint:

    def test_delete_existing_file(self, client):
        client.post("/upload", files={"file": ("delete_me.md", b"# bye", "text/markdown")})
        resp = client.delete("/delete/delete_me.md")
        assert resp.status_code == 200
        assert resp.json()["message"] == "Deleted successfully"

    def test_delete_nonexistent_file_returns_404(self, client):
        resp = client.delete("/delete/nope.md")
        assert resp.status_code == 404

    def test_delete_removes_file_from_list(self, client):
        client.post("/upload", files={"file": ("gone.md", b"# gone", "text/markdown")})
        client.delete("/delete/gone.md")
        resp = client.get("/list")
        filenames = [d["filename"] for d in resp.json()["documents"]]
        assert "gone.md" not in filenames
