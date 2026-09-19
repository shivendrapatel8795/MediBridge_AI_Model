from models import TriageRequest, Vitals
from triage import (
    triage_patient,
    get_triggered_rules,
    get_risk_factors,
    compare_human_decision,
    build_decision_comparison,
)


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

def test_human_decision_override():
    result = compare_human_decision(
        ai_urgency="high",
        ai_next_step="escalate",
        human_urgency="medium",
        human_next_step="teleconsult",
    )

    assert result["overridden"] is True
    assert result["urgencyChanged"] is True
    assert result["nextStepChanged"] is True

def test_human_decision_no_override():
    result = compare_human_decision(
        ai_urgency="high",
        ai_next_step="escalate",
        human_urgency="high",
        human_next_step="escalate",
    )

    assert result["overridden"] is False
    assert result["urgencyChanged"] is False
    assert result["nextStepChanged"] is False


def test_build_decision_comparison_with_override():
    result = build_decision_comparison(
        ai_urgency="high",
        ai_next_step="escalate",
        human_urgency="medium",
        human_next_step="teleconsult",
    )

    assert result["aiDecision"]["urgency"] == "high"
    assert result["aiDecision"]["nextStep"] == "escalate"

    assert result["humanDecision"]["urgency"] == "medium"
    assert result["humanDecision"]["nextStep"] == "teleconsult"

    assert result["comparison"]["overridden"] is True
    assert result["comparison"]["urgencyChanged"] is True
    assert result["comparison"]["nextStepChanged"] is True


def test_build_decision_comparison_without_override():
    result = build_decision_comparison(
        ai_urgency="high",
        ai_next_step="escalate",
        human_urgency="high",
        human_next_step="escalate",
    )

    assert result["comparison"]["overridden"] is False
    assert result["comparison"]["urgencyChanged"] is False
    assert result["comparison"]["nextStepChanged"] is False