from app.core.config import settings
from app.models.ecg import ECG
from app.models.lead import Lead
from app.models.user import Base, User

# This allows alembic to detect all models
__all__ = ["Base", "User", "ECG", "Lead"]
