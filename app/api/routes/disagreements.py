
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Evaluation, ReviewerDisagreement
from app.schemas.disagreement import (
    DisagreementCreate,
    DisagreementResolve,
)
from app.services.audit import create_audit_log


router = APIRouter()


@router.post("/")
def create_disagreement(
    data: DisagreementCreate,
    db: Session = Depends(get_db),
):
    evaluation = (
        db.query(Evaluation)
        .filter(Evaluation.id == data.evaluation_id)
        .first()
    )

    if evaluation is None:
        raise HTTPException(
            status_code=404,
            detail="Evaluation not found",
        )

    disagreement = ReviewerDisagreement(**data.model_dump())

    db.add(disagreement)
    db.commit()
    db.refresh(disagreement)

    create_audit_log(
        db=db,
        action="CREATE",
        entity_type="ReviewerDisagreement",
        entity_id=disagreement.id,
        description=f"Created reviewer disagreement for evaluation ID {disagreement.evaluation_id}",
    )

    return {
        "message": "Reviewer disagreement created successfully",
        "data": {
            "id": disagreement.id,
            "evaluation_id": disagreement.evaluation_id,
            "reviewer_1_score": disagreement.reviewer_1_score,
            "reviewer_2_score": disagreement.reviewer_2_score,
            "reviewer_1_notes": disagreement.reviewer_1_notes,
            "reviewer_2_notes": disagreement.reviewer_2_notes,
            "resolution_status": disagreement.resolution_status,
            "resolution_notes": disagreement.resolution_notes,
        },
    }


@router.get("/")
def get_disagreements(
    db: Session = Depends(get_db),
):
    disagreements = db.query(ReviewerDisagreement).all()

    return {
        "total": len(disagreements),
        "data": [
            {
                "id": item.id,
                "evaluation_id": item.evaluation_id,
                "reviewer_1_score": item.reviewer_1_score,
                "reviewer_2_score": item.reviewer_2_score,
                "reviewer_1_notes": item.reviewer_1_notes,
                "reviewer_2_notes": item.reviewer_2_notes,
                "resolution_status": item.resolution_status,
                "resolution_notes": item.resolution_notes,
            }
            for item in disagreements
        ],
    }


@router.get("/{disagreement_id}")
def get_disagreement(
    disagreement_id: int,
    db: Session = Depends(get_db),
):
    disagreement = (
        db.query(ReviewerDisagreement)
        .filter(ReviewerDisagreement.id == disagreement_id)
        .first()
    )

    if disagreement is None:
        raise HTTPException(
            status_code=404,
            detail="Disagreement not found",
        )

    return {
        "id": disagreement.id,
        "evaluation_id": disagreement.evaluation_id,
        "reviewer_1_score": disagreement.reviewer_1_score,
        "reviewer_2_score": disagreement.reviewer_2_score,
        "reviewer_1_notes": disagreement.reviewer_1_notes,
        "reviewer_2_notes": disagreement.reviewer_2_notes,
        "resolution_status": disagreement.resolution_status,
        "resolution_notes": disagreement.resolution_notes,
    }


@router.put("/{disagreement_id}/resolve")
def resolve_disagreement(
    disagreement_id: int,
    data: DisagreementResolve,
    db: Session = Depends(get_db),
):
    disagreement = (
        db.query(ReviewerDisagreement)
        .filter(ReviewerDisagreement.id == disagreement_id)
        .first()
    )

    if disagreement is None:
        raise HTTPException(
            status_code=404,
            detail="Disagreement not found",
        )

    disagreement.resolution_status = data.resolution_status
    disagreement.resolution_notes = data.resolution_notes

    db.commit()
    db.refresh(disagreement)

    create_audit_log(
        db=db,
        action="RESOLVE",
        entity_type="ReviewerDisagreement",
        entity_id=disagreement.id,
        description=f"Resolved reviewer disagreement for evaluation ID {disagreement.evaluation_id}",
    )

    return {
        "message": "Disagreement resolved successfully",
        "data": {
            "id": disagreement.id,
            "resolution_status": disagreement.resolution_status,
            "resolution_notes": disagreement.resolution_notes,
        },
    }
