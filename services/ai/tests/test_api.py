from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_primary_triage_api():
    payload = {
        "patientId": "PAT-1001",
        "age": 28,
        "sex": "F",
        "symptoms": [
            "fever",
            "cough",
            "breathing_difficulty"
        ],
        "vitals": {
            "tempC": 39.1,
            "spo2": 91,
            "hr": 118
        }
    }

    response = client.post("/triage", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert result["patientId"] == "PAT-1001"
    assert result["urgency"] == "high"
    assert result["nextStep"] == "escalate"

    assert "fever + breathing_difficulty" in result["triggeredRules"]
    assert "SpO2 < 94" in result["triggeredRules"]

    assert result["aiOnly"] is True
    assert result["disclaimer"] == (
        "AI recommends. Clinician decides. Not a diagnosis."
    )


def test_invalid_triage_request():
    payload = {
        "patientId": "",
        "age": 28,
        "sex": "F",
        "symptoms": ["fever"],
        "vitals": {
            "tempC": 39.1,
            "spo2": 91,
            "hr": 118
        }
    }

    response = client.post("/triage", json=payload)

    assert response.status_code == 400