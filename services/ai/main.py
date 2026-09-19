import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import DISCLAIMER, TRIAGE_RULE_VERSION
from models import (
    TriageRequest,
    TriageResponse,
    AuditInfo,
    ErrorResponse,
)
from validation import validate_triage_input, detect_missing_information
from triage import (
    triage_patient,
    get_triggered_rules,
    get_risk_factors,
    get_uncertainty,
    build_explanation,
    build_triage_timeline,
    build_risk_trend,
    get_follow_up_priority,
)
from reasons import generate_reason


app = FastAPI(
    title="MediBridge AI Triage Service",
    version="1.0",
    description="Deterministic AI-assisted triage decision-support service.",
)

@app.middleware("http")
async def monitor_performance(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time
    duration_ms = duration * 1000

    print(
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} "
        f"→ {duration_ms:.2f} ms"
    )

    response.headers["X-Process-Time-ms"] = f"{duration_ms:.2f}"

    return response


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
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid triage input.",
                "details": errors,
            },
        )

    # Apply MediBridge triage rules
    urgency, next_step = triage_patient(request)

    # Generate explanation
    reason = generate_reason(request, urgency)
    missing_information = detect_missing_information(request)
    triggered_rules = get_triggered_rules(request)
    risk_factors = get_risk_factors(request)
    uncertainty = get_uncertainty(request)
    explanation = build_explanation(request, urgency)
    timeline = build_triage_timeline()
    risk_trend = build_risk_trend([])
    follow_up = get_follow_up_priority(urgency)
    audit_info = AuditInfo(
        service="medibridge-ai",
        ruleVersion=TRIAGE_RULE_VERSION,
        aiOnly=True,
    )

    return TriageResponse(
        patientId=request.patientId,
        urgency=urgency,
        nextStep=next_step,
        reason=reason,
        missingInformation=missing_information,
        triggeredRules=triggered_rules,
        riskFactors=risk_factors,
        audit=audit_info,
        uncertainty=uncertainty,
        explanation=explanation,
        timeline=timeline,
        riskTrend=risk_trend,
        followUp=follow_up,
        aiOnly=True,
        disclaimer=DISCLAIMER,
    )