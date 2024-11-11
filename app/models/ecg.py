from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class ECG(Base):
    __tablename__ = "ecg"

    id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE")
    )
    date: Mapped[datetime.date] = mapped_column(Date)
    user: Mapped["User"] = relationship("User", back_populates="ecg")
    task_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), default=uuid4, nullable=True
    )
    leads: Mapped[list["Lead"]] = relationship(
        "Lead", back_populates="ecg", cascade="all, delete-orphan", lazy="joined"
    )
