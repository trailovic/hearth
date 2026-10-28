from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_success():
    with patch(
        "app.main.send_message",
        new_callable=AsyncMock,
        return_value="Hello from Beam!",
    ) as mock_send:

        response = client.post(
            "/api/chat",
            json={"message": "Hello!"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "response": "Hello from Beam!",
        "model": "beam:cloud",
    }

    mock_send.assert_awaited_once_with("Hello!")


def test_chat_empty_message():
    response = client.post(
        "/api/chat",
        json={"message": ""},
    )

    assert response.status_code == 422