import asyncio
from uuid import UUID

from app.celery.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.services.ecg import ECGService


def analyze_ecg_task(ecg_id: UUID, user_id: UUID):
    """Analyze ECG asynchronously."""
    return analyze_ecg.delay(str(ecg_id), str(user_id))

@celery_app.task(bind=True, max_retries=5)
def analyze_ecg(self, ecg_id: UUID, user_id: UUID):
    """Analyze ECG asynchronously."""
    try:
        asyncio.run(_analyze_ecg_task(ecg_id, user_id))
    except Exception as e:
        self.retry(exc=e, countdown=600)


async def _analyze_ecg_task(ecg_id: UUID, user_id: UUID):
    async with AsyncSessionLocal() as session:
        ecg_service = ECGService(session)
        ecg = await ecg_service.get_by_id(ecg_id, user_id)
        if not ecg:
            return {"status": "error", "message": "ECG not found"}

        analysis_result = await ecg_service.analyze_ecg(ecg)
        return {"status": "success", "ecg_id": str(ecg_id), "result": analysis_result}
