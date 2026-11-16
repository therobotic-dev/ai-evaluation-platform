
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Evaluation, Rubric
from app.schemas.evaluation import EvaluationCreate
from app.services.audit import create_audit_log


router = APIRouter()


def validate_rubric(db: Session, rubric_id: int | None):
    if rubric_id is not None:
        rubric = (
            db.query(Rubric)
            .filter(Rubric.id == rubric_id)
            .first()
        )

        if rubric is None:
            raise HTTPException(
                status_code=404,
                detail="Rubric not found",
            )


@router.post("/")
def create_evaluation(
    data: EvaluationCreate,
    db: Session = Depends(get_db),
):
    validate_rubric(db, data.rubric_id)

    evaluation = Evaluation(**data.model_dump())

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    create_audit_log(
        db=db,
        action="CREATE",
        entity_type="Evaluation",
        entity_id=evaluation.id,
        description=f"Created evaluation: {evaluation.task_name}",
    )

    return {
        "message": "Evaluation created successfully",
        "data": {
            "id": evaluation.id,
            "task_name": evaluation.task_name,
            "model_name": evaluation.model_name,
            "prompt": evaluation.prompt,
            "model_response": evaluation.model_response,
            "score": evaluation.score,
            "reviewer_notes": evaluation.reviewer_notes,
            "rubric_id": evaluation.rubric_id,
            "status": evaluation.status,
        },
    }


@router.get("/")
def get_evaluations(db: Session = Depends(get_db)):
    evaluations = db.query(Evaluation).all()

    evaluation_list = []

    for evaluation in evaluations:
        evaluation_list.append({
            "id": evaluation.id,
            "task_name": evaluation.task_name,
            "model_name": evaluation.model_name,
            "prompt": evaluation.prompt,
            "model_response": evaluation.model_response,
            "score": evaluation.score,
            "reviewer_notes": evaluation.reviewer_notes,
            "rubric_id": evaluation.rubric_id,
            "rubric_name": evaluation.rubric.name if evaluation.rubric else None,
            "status": evaluation.status,
        })

    return {
        "total": len(evaluation_list),
        "data": evaluation_list,
    }


@router.get("/{evaluation_id}")
def get_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
):
    evaluation = (
        db.query(Evaluation)
        .filter(Evaluation.id == evaluation_id)
        .first()
    )

    if evaluation is None:
        raise HTTPException(
            status_code=404,
            detail="Evaluation not found",
        )

    return {
        "id": evaluation.id,
        "task_name": evaluation.task_name,
        "model_name": evaluation.model_name,
        "prompt": evaluation.prompt,
        "model_response": evaluation.model_response,
        "score": evaluation.score,
        "reviewer_notes": evaluation.reviewer_notes,
        "rubric_id": evaluation.rubric_id,
        "rubric_name": evaluation.rubric.name if evaluation.rubric else None,
        "status": evaluation.status,
    }


@router.put("/{evaluation_id}")
def update_evaluation(
    evaluation_id: int,
    data: EvaluationCreate,
    db: Session = Depends(get_db),
):
    evaluation = (
        db.query(Evaluation)
        .filter(Evaluation.id == evaluation_id)
        .first()
    )

    if evaluation is None:
        raise HTTPException(
            status_code=404,
            detail="Evaluation not found",
        )

    validate_rubric(db, data.rubric_id)

    for field, value in data.model_dump().items():
        setattr(evaluation, field, value)

    db.commit()
    db.refresh(evaluation)

    create_audit_log(
        db=db,
        action="UPDATE",
        entity_type="Evaluation",
        entity_id=evaluation.id,
        description=f"Updated evaluation: {evaluation.task_name}",
    )

    return {
        "message": "Evaluation updated successfully",
        "data": {
            "id": evaluation.id,
            "task_name": evaluation.task_name,
            "model_name": evaluation.model_name,
            "prompt": evaluation.prompt,
            "model_response": evaluation.model_response,
            "score": evaluation.score,
            "reviewer_notes": evaluation.reviewer_notes,
            "rubric_id": evaluation.rubric_id,
            "status": evaluation.status,
        },
    }


@router.delete("/{evaluation_id}")
def delete_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
):
    evaluation = (
        db.query(Evaluation)
        .filter(Evaluation.id == evaluation_id)
        .first()
    )

    if evaluation is None:
        raise HTTPException(
            status_code=404,
            detail="Evaluation not found",
        )

    evaluation_task_name = evaluation.task_name
    deleted_id = evaluation.id

    db.delete(evaluation)
    db.commit()

    create_audit_log(
        db=db,
        action="DELETE",
        entity_type="Evaluation",
        entity_id=deleted_id,
        description=f"Deleted evaluation: {evaluation_task_name}",
    )

    return {
        "message": "Evaluation deleted successfully",
        "deleted_id": deleted_id,
    }
