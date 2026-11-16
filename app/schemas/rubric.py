
from pydantic import BaseModel, Field, model_validator


class RubricCriterionCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    weight: float = Field(..., ge=0, le=100)


class RubricCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    criteria: list[RubricCriterionCreate] = Field(
        ...,
        min_length=1,
    )

    @model_validator(mode="after")
    def validate_total_weight(self):
        total_weight = sum(
            criterion.weight for criterion in self.criteria
        )

        if total_weight != 100:
            raise ValueError(
                "The total weight of all criteria must equal 100."
            )

        return self
