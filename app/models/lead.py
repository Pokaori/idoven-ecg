from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.user import Base


class LeadName(StrEnum):
    I = "I"
    II = "II"
    III = "III"
    AVR = "aVR"
    AVL = "aVL"
    AVF = "aVF"
    V1 = "V1"
    V2 = "V2"
    V3 = "V3"
    V4 = "V4"
    V5 = "V5"
    V6 = "V6"


class Lead(Base):
    __tablename__ = "lead"

    id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ecg_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("ecg.id", ondelete="CASCADE")
    )
    name: Mapped[LeadName] = mapped_column(SQLAlchemyEnum(LeadName, native_enum=True))
    signal: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    sample_number: Mapped[int] = mapped_column(Integer,CheckConstraint('sample_number > 0', name="sample_number_con"), nullable=True)

    # Relationship
    ecg: Mapped["ECG"] = relationship("ECG", back_populates="leads")
    analysis: Mapped["ECGAnalysis"] = relationship(
        "ECGAnalysis",
        back_populates="lead",
        cascade="all, delete-orphan",
        lazy="joined",
    )
