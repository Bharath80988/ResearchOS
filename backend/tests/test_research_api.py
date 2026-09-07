import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_create_research_run(client):
    payload = {
        "question": "Can multimodal RAG improve educational assessment?",
        "intent": "academic_research",
        "depth": "deep"
    }
    response = client.post("/api/research", json=payload)
    assert response.status_code == 202
    data = response.get_json()
    assert "research_id" in data
    assert data["status"] == "queued"
    assert "stream_url" in data

    research_id = data["research_id"]

    # Test GET single run
    get_res = client.get(f"/api/research/{research_id}")
    assert get_res.status_code == 200
    run_data = get_res.get_json()
    assert run_data["id"] == research_id
    assert run_data["question"] == payload["question"]

    # Test GET events
    events_res = client.get(f"/api/research/{research_id}/events")
    assert events_res.status_code == 200
    events_data = events_res.get_json()
    assert "events" in events_data
    assert len(events_data["events"]) >= 1

def test_create_research_run_validation_error(client):
    # Missing required question
    response = client.post("/api/research", json={"depth": "deep"})
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
