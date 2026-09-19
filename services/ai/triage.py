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

def get_uncertainty(data):
    """Return a qualitative uncertainty level based on available input."""

    missing = []

    if data.vitals.tempC is None:
        missing.append("tempC")

    if data.vitals.spo2 is None:
        missing.append("spo2")

    if data.vitals.hr is None:
        missing.append("hr")

    # All required vital inputs available
    if not missing:
        return {
            "level": "low",
            "reason": "All supported vital inputs are available."
        }

    # Two or more vital inputs missing
    if len(missing) >= 2:
        return {
            "level": "high",
            "reason": "Multiple supported vital inputs are missing."
        }

    # One vital input missing
    return {
        "level": "medium",
        "reason": "One supported vital input is missing."
    }

def compare_human_decision(
    ai_urgency,
    ai_next_step,
    human_urgency,
    human_next_step,
):
    """Compare human decision with the AI recommendation."""

    urgency_changed = ai_urgency != human_urgency
    next_step_changed = ai_next_step != human_next_step

    return {
        "overridden": urgency_changed or next_step_changed,
        "urgencyChanged": urgency_changed,
        "nextStepChanged": next_step_changed,
    }

def build_explanation(data, urgency):
    """Build structured, visualization-friendly triage explanation."""

    return {
        "summary": generate_explanation_summary(data, urgency),
        "triggeredRules": get_triggered_rules(data),
        "riskFactors": get_risk_factors(data),
    }

def generate_explanation_summary(data, urgency):
    """Generate a short summary for visualization."""

    symptoms = {
        symptom.lower().strip()
        for symptom in data.symptoms
    }

    if urgency == "emergency":
        if "unconscious" in symptoms:
            return "Unconsciousness triggered the emergency recommendation."

        if "active_bleeding" in symptoms:
            return "Active bleeding triggered the emergency recommendation."

        if data.vitals.spo2 is not None and data.vitals.spo2 < 90:
            return "Very low oxygen saturation triggered the emergency recommendation."

    if urgency == "high":
        if (
            "fever" in symptoms
            and "breathing_difficulty" in symptoms
        ):
            return "Fever with breathing difficulty triggered the high-urgency recommendation."

        if data.vitals.spo2 is not None and data.vitals.spo2 < 94:
            return "Low oxygen saturation triggered the high-urgency recommendation."

        if data.vitals.tempC is not None and data.vitals.tempC >= 39:
            return "High temperature triggered the high-urgency recommendation."

    if urgency == "medium":
        if "fever" in symptoms:
            return "Fever triggered the medium-urgency recommendation."

        if "cough" in symptoms:
            return "Cough triggered the medium-urgency recommendation."

    return "No higher-priority triage rule was triggered."


def build_decision_comparison(
    ai_urgency,
    ai_next_step,
    human_urgency,
    human_next_step,
):
    """Build a structured AI vs human decision comparison."""

    comparison = compare_human_decision(
        ai_urgency,
        ai_next_step,
        human_urgency,
        human_next_step,
    )

    return {
        "aiDecision": {
            "urgency": ai_urgency,
            "nextStep": ai_next_step,
        },
        "humanDecision": {
            "urgency": human_urgency,
            "nextStep": human_next_step,
        },
        "comparison": comparison,
    }

def build_triage_timeline():
    """Build the sequence of events for the current AI triage process."""

    return [
        {
            "event": "triage_received",
            "description": "Patient symptoms and supported vital information received.",
        },
        {
            "event": "ai_assessment",
            "description": "Deterministic triage rules were evaluated.",
        },
        {
            "event": "ai_recommendation",
            "description": "AI recommendation generated.",
        },
    ]

def build_risk_trend(assessment_history):
    """Convert existing assessment history into a visualization-friendly trend."""

    trend = []

    for index, assessment in enumerate(assessment_history, start=1):
        trend.append({
            "assessment": index,
            "urgency": assessment,
        })

    return trend

def get_follow_up_priority(urgency):
    """Derive a qualitative follow-up priority from the existing urgency."""

    if urgency in ("emergency", "high"):
        return {
            "priority": "urgent",
            "reason": "The current triage urgency requires priority follow-up."
        }

    if urgency == "medium":
        return {
            "priority": "priority",
            "reason": "The current triage urgency indicates priority follow-up."
        }

    return {
        "priority": "routine",
        "reason": "The current triage urgency indicates routine follow-up."
    }