from typing import Annotated

from pydantic import UUID4, BaseModel, ConfigDict, Field

from app.models.lead import LeadName
from app.schemas.analysis import ECGAnalysisOut


class LeadBase(BaseModel):
    name: LeadName
    signal: list[int]
    sample_number: Annotated[int, Field(strict=True, gt=0)] | None = None

class LeadCreate(LeadBase):
    pass


class LeadOut(LeadBase):
    id: UUID4
    analysis: ECGAnalysisOut | None = None

    model_config = ConfigDict(from_attributes=True)
