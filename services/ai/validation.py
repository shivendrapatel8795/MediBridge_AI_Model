def validate_triage_input(data):
    """Validate basic, non-clinical triage input."""

    errors = []

    # Patient ID
    if not data.patientId.strip():
        errors.append("patientId is required.")

    # Age
    if data.age < 0:
        errors.append("age cannot be negative.")

    # Sex
    if not data.sex.strip():
        errors.append("sex is required.")

    # Basic vital-sign input validation
    if data.vitals.tempC is not None:
        if data.vitals.tempC < 0 or data.vitals.tempC > 50:
            errors.append("tempC must be between 0 and 50.")

    if data.vitals.spo2 is not None:
        if data.vitals.spo2 < 0 or data.vitals.spo2 > 100:
            errors.append("spo2 must be between 0 and 100.")

    if data.vitals.hr is not None:
        if data.vitals.hr < 0:
            errors.append("hr cannot be negative.")

    if errors:
        return False, errors

    return True, []

def detect_missing_information(data):
    """Identify missing non-diagnostic triage information."""

    missing = []

    if data.vitals.tempC is None:
        missing.append("tempC")

    if data.vitals.spo2 is None:
        missing.append("spo2")

    if data.vitals.hr is None:
        missing.append("hr")

    return missing