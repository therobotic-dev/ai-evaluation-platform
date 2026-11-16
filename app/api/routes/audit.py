
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import AuditLog


router = APIRouter()


@router.get("/")
def get_audit_logs(
    db: Session = Depends(get_db),
):
    audit_logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return {
        "total": len(audit_logs),
        "data": [
            {
                "id": item.id,
                "action": item.action,
                "entity_type": item.entity_type,
                "entity_id": item.entity_id,
                "description": item.description,
                "created_at": item.created_at,
            }
            for item in audit_logs
        ],
    }
