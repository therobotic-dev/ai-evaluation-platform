
from sqlalchemy.orm import Session

from app.database.models import AuditLog


def create_audit_log(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: int | None,
    description: str,
):
    audit_log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log
