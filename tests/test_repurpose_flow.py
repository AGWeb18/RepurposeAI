from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app, calendar
from app.schemas.content import RepurposeChannel


client = TestClient(app)


def test_ingest_and_repurpose_flow():
    payload = {
        "title": "Winning the content repurposing game",
        "body": """Creators feel stuck repurposing content.\nRepurposeAI extracts highlights.\nThe result is more reach without burnout.""",
        "source_type": "podcast",
        "duration_minutes": 42,
        "tags": ["growth", "ai"],
        "brand_voice_id": "default",
    }
    response = client.post("/ingest", json=payload)
    assert response.status_code == 200
    content_id = response.json()["content_id"]

    calendar.reset()
    repurpose_payload = {
        "content_id": content_id,
        "channels": [
            RepurposeChannel.TIKTOK.value,
            RepurposeChannel.X_THREAD.value,
            RepurposeChannel.NEWSLETTER_SUMMARY.value,
        ],
        "cadence_days": 2,
        "primary_cta": "Join the waitlist",
    }
    repurpose_response = client.post("/repurpose", json=repurpose_payload)
    assert repurpose_response.status_code == 200
    data = repurpose_response.json()

    assert data["content_id"] == content_id
    assert len(data["assets"]) == 3

    scheduled_times = [datetime.fromisoformat(asset["scheduled_for"]) for asset in data["assets"]]
    assert scheduled_times == sorted(scheduled_times)
    for asset in data["assets"]:
        assert "Join the waitlist" in asset["body"] or "Tone cues" in asset["body"]
        assert asset["brand_voice_id"] == "default"
