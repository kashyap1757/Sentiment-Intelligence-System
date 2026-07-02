from fastapi.testclient import TestClient
from sentiment_intelligence.api.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
