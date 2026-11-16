
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.database.models import Evaluation, Rubric


router = APIRouter()


@router.get("/summary")
def get_analytics_summary(
    db: Session = Depends(get_db),
):
    total_evaluations = db.query(Evaluation).count()

    pending_count = (
        db.query(Evaluation)
        .filter(Evaluation.status == "Pending")
        .count()
    )

    in_review_count = (
        db.query(Evaluation)
        .filter(Evaluation.status == "In Review")
        .count()
    )

    completed_count = (
        db.query(Evaluation)
        .filter(Evaluation.status == "Completed")
        .count()
    )

    average_score = (
        db.query(func.avg(Evaluation.score))
        .scalar()
    )

    return {
        "total_evaluations": total_evaluations,
        "status_summary": {
            "Pending": pending_count,
            "In Review": in_review_count,
            "Completed": completed_count,
        },
        "average_score": (
            round(average_score, 2)
            if average_score is not None
            else None
        ),
    }


@router.get("/rubric-quality")
def get_rubric_quality(
    db: Session = Depends(get_db),
):
    rubrics = db.query(Rubric).all()

    quality_summary = []

    for rubric in rubrics:
        total_evaluations = (
            db.query(Evaluation)
            .filter(Evaluation.rubric_id == rubric.id)
            .count()
        )

        average_score = (
            db.query(func.avg(Evaluation.score))
            .filter(Evaluation.rubric_id == rubric.id)
            .scalar()
        )

        quality_summary.append({
            "rubric_id": rubric.id,
            "rubric_name": rubric.name,
            "total_evaluations": total_evaluations,
            "average_score": (
                round(average_score, 2)
                if average_score is not None
                else None
            ),
        })

    return {
        "total_rubrics": len(rubrics),
        "data": quality_summary,
    }
