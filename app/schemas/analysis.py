from pydantic import UUID4, BaseModel, ConfigDict


class ECGAnalysisBase(BaseModel):

    result: int


class ECGAnalysisOut(ECGAnalysisBase):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)
