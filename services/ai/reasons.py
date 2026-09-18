def generate_reason(data, urgency):
    """Generate a short, non-diagnostic explanation."""

    symptoms = {symptom.lower().strip() for symptom in data.symptoms}

    temp = data.vitals.tempC
    spo2 = data.vitals.spo2
    hr = data.vitals.hr

    has_fever = "fever" in symptoms
    has_cough = "cough" in symptoms
    has_breathing_difficulty = "breathing_difficulty" in symptoms
    is_unconscious = "unconscious" in symptoms
    has_active_bleeding = "active_bleeding" in symptoms

    if urgency == "emergency":
        if is_unconscious:
            return "Unconsciousness requires immediate clinician attention."
        if has_active_bleeding:
            return "Active bleeding requires immediate clinician attention."
        if spo2 is not None and spo2 < 90:
            return "Very low oxygen saturation requires immediate clinician attention."

    if urgency == "high":
        if has_fever and has_breathing_difficulty:
            return "Fever with breathing difficulty requires prompt clinician review."
        if spo2 is not None and spo2 < 94:
            return "Low oxygen saturation requires prompt clinician review."
        if temp is not None and temp >= 39:
            return "High temperature requires prompt clinician review."
        if has_fever and has_cough and hr is not None and hr >= 110:
            return "Fever, cough, and elevated heart rate require prompt clinician review."

    if urgency == "medium":
        if has_fever:
            return "Fever requires clinician review through the recommended next step."
        if has_cough:
            return "Cough requires clinician review through the recommended next step."
        if temp is not None and temp >= 38:
            return "Elevated temperature requires clinician review through the recommended next step."

    return "No higher-priority triage rule was triggered; routine care may be appropriate."