from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import DISCLAIMER
from models import TriageRequest, TriageResponse
from validation import validate_triage_input, detect_missing_information
from triage import (
    triage_patient,
    get_triggered_rules,
    get_risk_factors,
)
from reasons import generate_reason


app = FastAPI(
    title="MediBridge AI Triage Service",
    version="1.0",
    description="Deterministic AI-assisted triage decision-support service.",
)


# CORS: Worker App ko AI API call karne ki permission
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/triage", response_model=TriageResponse)
def triage(request: TriageRequest):
    # Basic input validation
    is_valid, errors = validate_triage_input(request)

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=errors,
        )

    # Apply MediBridge triage rules
    urgency, next_step = triage_patient(request)

    # Generate explanation
    reason = generate_reason(request, urgency)
    missing_information = detect_missing_information(request)
    triggered_rules = get_triggered_rules(request)
    risk_factors = get_risk_factors(request)

    return TriageResponse(
        patientId=request.patientId,
        urgency=urgency,
        nextStep=next_step,
        reason=reason,
        missingInformation=missing_information,
        triggeredRules=triggered_rules,
        riskFactors=risk_factors,
        aiOnly=True,
        disclaimer=DISCLAIMER,
    )