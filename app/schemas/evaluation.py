
from pydantic import BaseModel, Field


class EvaluationCreate(BaseModel):
    task_name: str = Field(..., min_length=1)
    model_name: str = Field(..., min_length=1)
    prompt: str = Field(..., min_length=1)
    model_response: str = Field(..., min_length=1)

    score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    reviewer_notes: str | None = None
    rubric_id: int | None = None

    status: str = Field(
        default="Pending",
        pattern="^(Pending|In Review|Completed)$",
    )
