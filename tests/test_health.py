from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_requires_api_key():
    response = client.post("/search", json={"query": "test", "top_k": 3})
    assert response.status_code == 401
