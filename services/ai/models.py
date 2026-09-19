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


class AuditInfo(BaseModel):
    service: str
    ruleVersion: str
    aiOnly: bool


class UncertaintyInfo(BaseModel):
    level: Literal[
        "low",
        "medium",
        "high",
    ]
    reason: str

class ExplanationInfo(BaseModel):
    summary: str
    triggeredRules: List[str]
    riskFactors: List[str]

class DecisionInfo(BaseModel):
    urgency: Urgency
    nextStep: NextStep


class DecisionComparison(BaseModel):
    aiDecision: DecisionInfo
    humanDecision: DecisionInfo
    comparison: dict

class TimelineEvent(BaseModel):
    event: str
    description: str

class RiskTrendPoint(BaseModel):
    assessment: int
    urgency: Urgency

class FollowUpInfo(BaseModel):
    priority: Literal[
        "routine",
        "priority",
        "urgent",
    ]
    reason: str

class TriageResponse(BaseModel):
    patientId: str
    urgency: Urgency
    nextStep: NextStep
    reason: str
    missingInformation: List[str]
    triggeredRules: List[str]
    riskFactors: List[str]
    audit: AuditInfo
    uncertainty: UncertaintyInfo
    explanation: ExplanationInfo
    timeline: List[TimelineEvent]
    riskTrend: List[RiskTrendPoint]
    followUp: FollowUpInfo
    aiOnly: bool
    disclaimer: str

class ErrorResponse(BaseModel):
    error: str
    details: List[str]