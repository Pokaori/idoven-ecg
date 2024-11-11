from typing import List
from uuid import UUID

from celery.result import AsyncResult
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.analysis import ECGAnalysis
from app.models.ecg import ECG
from app.models.lead import Lead
from app.schemas.ecg import CeleryTaskStatus, ECGCreate
from app.services.base import BaseService


class ECGService(BaseService):
    async def get_by_id(self, ecg_id: UUID, user_id: UUID) -> ECG | None:
        result = await self.db.execute(
            select(ECG)
            .options(selectinload(ECG.leads))
            .where((ECG.id == ecg_id) & (ECG.user_id == user_id))
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: UUID, ecg_in: ECGCreate) -> ECG:
        """Create new ECG with leads and trigger analysis."""
        ecg = ECG(
            user_id=user_id,
            date=ecg_in.date,
            leads=[
                Lead(
                    name=lead_data.name,
                    signal=lead_data.signal,
                    sample_number=lead_data.sample_number,
                )
                for lead_data in ecg_in.leads
            ],
        )
        self.db.add(ecg)
        await self.commit()
        await self.refresh(ecg)
        return ecg

    async def update_task_id(self, ecg_id: UUID, task_id: str, user_id: UUID) -> ECG:
        ecg = await self.get_by_id(ecg_id, user_id)
        ecg.task_id = task_id
        await self.commit()
        await self.refresh(ecg)
        return ecg

    async def analyze_ecg(self, ecg: ECG) -> ECG:
        """Calculate zero crossings for each lead in the ECG."""
        for lead in ecg.leads:
            zero_crossings = await self._count_zero_crossings(lead.signal)
            analysis_item = ECGAnalysis(lead_id=lead.id, result=zero_crossings)
            lead.analysis = analysis_item
        await self.commit()
        await self.refresh(ecg)

        return ecg

    async def _count_zero_crossings(self, signal: list[int]) -> int:
        """Count the number of times the signal crosses zero."""
        crossings = 0
        for i, value in enumerate(signal[:-1]):
            next_value = signal[i + 1]
            if (value >= 0 and next_value < 0) or (value < 0 and next_value >= 0):
                crossings += 1
        return crossings

    async def get_analysis_status(self, task_id: str) -> CeleryTaskStatus:
        """Get the status of an analysis task."""
        result = AsyncResult(str(task_id))
        return CeleryTaskStatus(
            task_id=task_id,
            status=result.status,
        )
