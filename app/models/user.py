from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.security import verify_password
from app.db.base_class import Base
from app.models.base import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    ecg: Mapped[list["ECG"]] = relationship(
        "ECG", back_populates="user", cascade="all, delete-orphan"
    )

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)
