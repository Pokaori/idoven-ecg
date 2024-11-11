from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class ECGAnalysis(Base):
    __tablename__ = "ecg_analysis"

    id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    lead_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("lead.id", ondelete="CASCADE")
    )
    result: Mapped[str] = mapped_column(Integer)

    lead: Mapped["Lead"] = relationship(
        "Lead",
        back_populates="analysis",
    )
