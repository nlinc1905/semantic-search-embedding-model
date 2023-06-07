from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_embed():
    text = "string"
    response = client.post("/embed", json={
        "text": text
    })
    assert response.status_code == 200


def test_embed_batch():
    texts = ["apples", "bananas"]
    response = client.post("/embed_batch", json={
        "texts": texts
    })
    assert response.status_code == 200
