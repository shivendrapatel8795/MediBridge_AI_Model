def triage_patient(data):
    """
    Apply the MediBridge deterministic triage rules.

    Priority:
    1. Emergency
    2. High
    3. Medium
    4. Low
    """

    symptoms = {symptom.lower().strip() for symptom in data.symptoms}

    temp = data.vitals.tempC
    spo2 = data.vitals.spo2
    hr = data.vitals.hr

    has_fever = "fever" in symptoms
    has_cough = "cough" in symptoms
    has_breathing_difficulty = "breathing_difficulty" in symptoms
    is_unconscious = "unconscious" in symptoms
    has_active_bleeding = "active_bleeding" in symptoms

    # 1. Emergency
    if (
        is_unconscious
        or has_active_bleeding
        or (spo2 is not None and spo2 < 90)
    ):
        return "emergency", "emergency"

    # 2. High
    if (
        (has_fever and has_breathing_difficulty)
        or (spo2 is not None and spo2 < 94)
        or (temp is not None and temp >= 39)
        or (has_fever and has_cough and hr is not None and hr >= 110)
    ):
        return "high", "escalate"

    # 3. Medium
    if (
        has_fever
        or has_cough
        or (temp is not None and temp >= 38)
    ):
        return "medium", "teleconsult"

    # 4. Low
    return "low", "stay"

def get_triggered_rules(data):
    """Return the deterministic rules triggered by the input."""

    symptoms = {symptom.lower().strip() for symptom in data.symptoms}

    temp = data.vitals.tempC
    spo2 = data.vitals.spo2
    hr = data.vitals.hr

    has_fever = "fever" in symptoms
    has_cough = "cough" in symptoms
    has_breathing_difficulty = "breathing_difficulty" in symptoms
    is_unconscious = "unconscious" in symptoms
    has_active_bleeding = "active_bleeding" in symptoms

    triggered = []

    if is_unconscious:
        triggered.append("unconscious")

    if has_active_bleeding:
        triggered.append("active_bleeding")

    if spo2 is not None and spo2 < 90:
        triggered.append("SpO2 < 90")

    if has_fever and has_breathing_difficulty:
        triggered.append("fever + breathing_difficulty")

    if spo2 is not None and spo2 < 94:
        triggered.append("SpO2 < 94")

    if temp is not None and temp >= 39:
        triggered.append("temperature >= 39")

    if has_fever and has_cough and hr is not None and hr >= 110:
        triggered.append("fever + cough + HR >= 110")

    if has_fever:
        triggered.append("fever")

    if has_cough:
        triggered.append("cough")

    if temp is not None and temp >= 38:
        triggered.append("temperature >= 38")

    return triggered

def get_risk_factors(data):
    """Return risk factors derived from existing triage inputs and rules."""

    symptoms = {symptom.lower().strip() for symptom in data.symptoms}

    temp = data.vitals.tempC
    spo2 = data.vitals.spo2
    hr = data.vitals.hr

    risk_factors = []

    if "unconscious" in symptoms:
        risk_factors.append("unconscious")

    if "active_bleeding" in symptoms:
        risk_factors.append("active bleeding")

    if "breathing_difficulty" in symptoms:
        risk_factors.append("breathing difficulty")

    if spo2 is not None and spo2 < 94:
        risk_factors.append("low oxygen saturation")

    if temp is not None and temp >= 39:
        risk_factors.append("high temperature")

    if "fever" in symptoms:
        risk_factors.append("fever")

    if "cough" in symptoms:
        risk_factors.append("cough")

    if hr is not None and hr >= 110:
        risk_factors.append("elevated heart rate")

    return risk_factors