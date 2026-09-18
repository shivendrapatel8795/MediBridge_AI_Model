from typing import List, Literal, Optional

from pydantic import BaseModel


Urgency = Literal[
    "low",
    "medium",
    "high",
    "emergency",
]

NextStep = Literal[
    "stay",
    "teleconsult",
    "escalate",
    "emergency",
]


class Vitals(BaseModel):
    tempC: Optional[float] = None
    spo2: Optional[float] = None
    hr: Optional[int] = None


class TriageRequest(BaseModel):
    patientId: str
    age: int
    sex: str
    symptoms: List[str]
    vitals: Vitals


class TriageResponse(BaseModel):
    patientId: str
    urgency: Urgency
    nextStep: NextStep
    reason: str
    missingInformation: List[str]
    triggeredRules: List[str]
    riskFactors: List[str]
    aiOnly: bool
    disclaimer: str