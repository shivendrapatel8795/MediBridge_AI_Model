from models import TriageRequest, Vitals
from triage import triage_patient, get_triggered_rules, get_risk_factors


def test_primary_case():
    data = TriageRequest(
        patientId="PAT-1001",
        age=28,
        sex="F",
        symptoms=["fever", "cough", "breathing_difficulty"],
        vitals=Vitals(
            tempC=39.1,
            spo2=91,
            hr=118,
        ),
    )

    urgency, next_step = triage_patient(data)

    assert urgency == "high"
    assert next_step == "escalate"


def test_mild_case():
    data = TriageRequest(
        patientId="TEST-MILD",
        age=25,
        sex="M",
        symptoms=["cough"],
        vitals=Vitals(
            tempC=37.2,
            spo2=98,
            hr=None,
        ),
    )

    urgency, next_step = triage_patient(data)

    assert urgency in ("medium", "low")


def test_emergency_case():
    data = TriageRequest(
        patientId="TEST-EMERGENCY",
        age=40,
        sex="M",
        symptoms=[],
        vitals=Vitals(
            tempC=37.0,
            spo2=88,
            hr=90,
        ),
    )

    urgency, next_step = triage_patient(data)

    assert urgency == "emergency"
    assert next_step == "emergency"

def test_triggered_rules():
    data = TriageRequest(
        patientId="TEST-RULES",
        age=28,
        sex="F",
        symptoms=[
            "fever",
            "cough",
            "breathing_difficulty"
        ],
        vitals=Vitals(
            tempC=39.1,
            spo2=91,
            hr=118,
        ),
    )

    triggered = get_triggered_rules(data)

    assert "fever + breathing_difficulty" in triggered
    assert "SpO2 < 94" in triggered
    assert "temperature >= 39" in triggered
    assert "fever + cough + HR >= 110" in triggered

def test_risk_factors():
    data = TriageRequest(
        patientId="TEST-RISK",
        age=28,
        sex="F",
        symptoms=[
            "fever",
            "cough",
            "breathing_difficulty"
        ],
        vitals=Vitals(
            tempC=39.1,
            spo2=91,
            hr=118,
        ),
    )

    risk_factors = get_risk_factors(data)

    assert "breathing difficulty" in risk_factors
    assert "low oxygen saturation" in risk_factors
    assert "high temperature" in risk_factors
    assert "fever" in risk_factors
    assert "cough" in risk_factors
    assert "elevated heart rate" in risk_factors