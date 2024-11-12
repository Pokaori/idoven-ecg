from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api import deps
from app.celery.worker import analyze_ecg_task
from app.models.user import User
from app.schemas.ecg import ECGCreate, ECGOutLeads, ECGTaskOut
from app.services.ecg import ECGService

router = APIRouter()


@router.post("", response_model=ECGOutLeads)
async def create_ecg(
    *,
    ecg: ECGCreate,
    current_user: Annotated[User, Depends(deps.get_common_user)],
    ecg_service: Annotated[ECGService, Depends()],
) -> ECGOutLeads:
    """Create new ECG."""
    ecg = await ecg_service.create(current_user.id, ecg)
    task = analyze_ecg_task(ecg.id,current_user.id)
    ecg = await ecg_service.update_task_id(ecg.id, task.id, current_user.id)
    return ecg


@router.get("/{ecg_id}", response_model=ECGTaskOut)
async def get_ecg(
    ecg_id: UUID,
    current_user: Annotated[User, Depends(deps.get_common_user)],
    ecg_service: Annotated[ECGService, Depends()],
) -> ECGTaskOut:
    """
    Get a specific ECG by ID.
    """
    ecg = await ecg_service.get_by_id(ecg_id, current_user.id)
    task = await ecg_service.get_analysis_status(ecg.task_id) if ecg.task_id else None
    if not ecg:
        raise HTTPException(status_code=404, detail="ECG not found")
    return ECGTaskOut(ecg=ecg, task=task)
