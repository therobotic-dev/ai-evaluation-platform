
from pydantic import BaseModel, Field


class DisagreementCreate(BaseModel):
    evaluation_id: int = Field(..., gt=0)

    reviewer_1_score: float = Field(
        ...,
        ge=0,
        le=100,
    )

    reviewer_2_score: float = Field(
        ...,
        ge=0,
        le=100,
    )

    reviewer_1_notes: str | None = None
    reviewer_2_notes: str | None = None

    resolution_status: str = Field(
        default="Pending",
        pattern="^(Pending|Resolved)$",
    )

    resolution_notes: str | None = None


class DisagreementResolve(BaseModel):
    resolution_status: str = Field(
        default="Resolved",
        pattern="^Resolved$",
    )

    resolution_notes: str = Field(
        ...,
        min_length=1,
    )
