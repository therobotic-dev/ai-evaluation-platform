
from datetime import datetime

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    rubric_id = Column(
        Integer,
        ForeignKey("rubrics.id"),
        nullable=True,
    )

    rubric = relationship("Rubric")

    task_name = Column(String(255), nullable=False)
    model_name = Column(String(255), nullable=False)
    prompt = Column(Text, nullable=False)
    model_response = Column(Text, nullable=False)
    score = Column(Float, nullable=True)
    reviewer_notes = Column(Text, nullable=True)

    status = Column(
        String(50),
        nullable=False,
        default="Pending",
    )


class Rubric(Base):
    __tablename__ = "rubrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    criteria = relationship(
        "RubricCriterion",
        back_populates="rubric",
        cascade="all, delete-orphan",
    )


class RubricCriterion(Base):
    __tablename__ = "rubric_criteria"

    id = Column(Integer, primary_key=True, index=True)

    rubric_id = Column(
        Integer,
        ForeignKey("rubrics.id"),
        nullable=False,
    )

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    weight = Column(Float, nullable=False)

    rubric = relationship(
        "Rubric",
        back_populates="criteria",
    )


class ReviewerDisagreement(Base):
    __tablename__ = "reviewer_disagreements"

    id = Column(Integer, primary_key=True, index=True)

    evaluation_id = Column(
        Integer,
        ForeignKey("evaluations.id"),
        nullable=False,
    )

    reviewer_1_score = Column(Float, nullable=False)
    reviewer_2_score = Column(Float, nullable=False)

    reviewer_1_notes = Column(Text, nullable=True)
    reviewer_2_notes = Column(Text, nullable=True)

    resolution_status = Column(
        String(50),
        nullable=False,
        default="Pending",
    )

    resolution_notes = Column(Text, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)

    description = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
