# MediBridge AI Triage Service

MediBridge AI Triage Service is a deterministic decision-support API for the MediBridge platform.

It receives patient symptoms and basic vital signs from the frontline worker application and returns:

- urgency level
- recommended next step
- short non-diagnostic reason
- AI-only flag
- safety disclaimer

The service supports clinician decision-making. It does not diagnose diseases or replace a clinician.

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTTPX

Default server port:

```text
8000