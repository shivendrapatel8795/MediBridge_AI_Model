from models import TriageRequest, Vitals
from validation import validate_triage_input, detect_missing_information


def test_valid_input():
    data = TriageRequest(
        patientId="PAT-1001",
        age=28,
        sex="F",
        symptoms=["fever"],
        vitals=Vitals(
            tempC=39.1,
            spo2=91,
            hr=118,
        ),
    )

    is_valid, errors = validate_triage_input(data)

    assert is_valid is True
    assert errors == []


def test_missing_patient_id():
    data = TriageRequest(
        patientId="",
        age=28,
        sex="F",
        symptoms=["fever"],
        vitals=Vitals(
            tempC=39.1,
            spo2=91,
            hr=118,
        ),
    )

    is_valid, errors = validate_triage_input(data)

    assert is_valid is False
    assert "patientId is required." in errors


def test_negative_age():
    data = TriageRequest(
        patientId="TEST-001",
        age=-1,
        sex="M",
        symptoms=["cough"],
        vitals=Vitals(
            tempC=37.2,
            spo2=98,
            hr=None,
        ),
    )

    is_valid, errors = validate_triage_input(data)

    assert is_valid is False
    assert "age cannot be negative." in errors


def test_empty_symptoms_allowed_for_vital_based_triage():
    data = TriageRequest(
        patientId="TEST-003",
        age=40,
        sex="M",
        symptoms=[],
        vitals=Vitals(
            tempC=37.0,
            spo2=88,
            hr=90,
        ),
    )

    is_valid, errors = validate_triage_input(data)

    assert is_valid is True
    assert errors == []

def test_invalid_temperature():
    data = TriageRequest(
        patientId="TEST-TEMP",
        age=30,
        sex="M",
        symptoms=["fever"],
        vitals=Vitals(
            tempC=60,
            spo2=98,
            hr=80,
        ),
    )

    is_valid, errors = validate_triage_input(data)

    assert is_valid is False
    assert "tempC must be between 0 and 50." in errors


def test_invalid_spo2():
    data = TriageRequest(
        patientId="TEST-SPO2",
        age=30,
        sex="M",
        symptoms=["cough"],
        vitals=Vitals(
            tempC=37,
            spo2=120,
            hr=80,
        ),
    )

    is_valid, errors = validate_triage_input(data)

    assert is_valid is False
    assert "spo2 must be between 0 and 100." in errors


def test_negative_heart_rate():
    data = TriageRequest(
        patientId="TEST-HR",
        age=30,
        sex="M",
        symptoms=["cough"],
        vitals=Vitals(
            tempC=37,
            spo2=98,
            hr=-10,
        ),
    )

    is_valid, errors = validate_triage_input(data)

    assert is_valid is False
    assert "hr cannot be negative." in errors

def test_detect_missing_vitals():
    data = TriageRequest(
        patientId="TEST-MISSING",
        age=30,
        sex="M",
        symptoms=["cough"],
        vitals=Vitals(
            tempC=None,
            spo2=None,
            hr=80,
        ),
    )

    missing = detect_missing_information(data)

    assert missing == ["tempC", "spo2"]