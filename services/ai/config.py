"""Shared configuration and locked MediBridge AI contracts."""

TRIAGE_RULE_VERSION = "1.0"

URGENCY_VALUES = (
    "low",
    "medium",
    "high",
    "emergency",
)

NEXT_STEP_VALUES = (
    "stay",
    "teleconsult",
    "escalate",
    "emergency",
)

DISCLAIMER = "AI recommends. Clinician decides. Not a diagnosis."