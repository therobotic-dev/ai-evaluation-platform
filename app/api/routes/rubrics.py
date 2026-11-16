
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Rubric, RubricCriterion
from app.schemas.rubric import RubricCreate


router = APIRouter()


@router.post("/")
def create_rubric(
    data: RubricCreate,
    db: Session = Depends(get_db),
):
    rubric = Rubric(
        name=data.name,
        description=data.description,
        criteria=[
            RubricCriterion(**criterion.model_dump())
            for criterion in data.criteria
        ],
    )

    db.add(rubric)
    db.commit()
    db.refresh(rubric)

    return {
        "message": "Rubric created successfully",
        "data": {
            "id": rubric.id,
            "name": rubric.name,
            "description": rubric.description,
            "criteria": [
                {
                    "id": criterion.id,
                    "name": criterion.name,
                    "description": criterion.description,
                    "weight": criterion.weight,
                }
                for criterion in rubric.criteria
            ],
        },
    }


@router.get("/")
def get_rubrics(db: Session = Depends(get_db)):
    rubrics = db.query(Rubric).all()

    return {
        "total": len(rubrics),
        "data": [
            {
                "id": rubric.id,
                "name": rubric.name,
                "description": rubric.description,
                "criteria": [
                    {
                        "id": criterion.id,
                        "name": criterion.name,
                        "description": criterion.description,
                        "weight": criterion.weight,
                    }
                    for criterion in rubric.criteria
                ],
            }
            for rubric in rubrics
        ],
    }

@router.put("/{rubric_id}")
def update_rubric(
    rubric_id: int,
    data: RubricCreate,
    db: Session = Depends(get_db),
):
    rubric = db.query(Rubric).filter(
        Rubric.id == rubric_id
    ).first()

    if rubric is None:
        raise HTTPException(
            status_code=404,
            detail="Rubric not found",
        )

    rubric.name = data.name
    rubric.description = data.description

    rubric.criteria.clear()

    for criterion in data.criteria:
        rubric.criteria.append(
            RubricCriterion(**criterion.model_dump())
        )

    db.commit()
    db.refresh(rubric)

    return {
        "message": "Rubric updated successfully",
        "data": {
            "id": rubric.id,
            "name": rubric.name,
            "description": rubric.description,
            "criteria": [
                {
                    "id": criterion.id,
                    "name": criterion.name,
                    "description": criterion.description,
                    "weight": criterion.weight,
                }
                for criterion in rubric.criteria
            ],
        },
    }

@router.delete("/{rubric_id}")
def delete_rubric(
    rubric_id: int,
    db: Session = Depends(get_db),
):
    rubric = db.query(Rubric).filter(
        Rubric.id == rubric_id
    ).first()

    if rubric is None:
        raise HTTPException(
            status_code=404,
            detail="Rubric not found",
        )

    db.delete(rubric)
    db.commit()

    return {
        "message": "Rubric deleted successfully",
        "deleted_id": rubric_id,
    }
