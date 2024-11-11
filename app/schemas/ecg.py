from datetime import date

from pydantic import UUID4, BaseModel, ConfigDict

from app.schemas.lead import LeadCreate, LeadOut


class ECGBase(BaseModel):
    date: date


class ECGCreate(ECGBase):
    leads: list[LeadCreate]


class ECGOut(ECGBase):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)


class ECGOutLeads(ECGOut):
    leads: list[LeadOut]


class CeleryTaskStatus(BaseModel):
    task_id: UUID4
    status: str


class ECGTaskOut(BaseModel):
    ecg: ECGOutLeads
    task: CeleryTaskStatus | None
