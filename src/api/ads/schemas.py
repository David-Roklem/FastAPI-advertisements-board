from pydantic import UUID4, BaseModel, ConfigDict, Field


class AdBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=100, max_length=1000)
    type: str = Field(..., min_length=3, max_length=150)


class CreateAd(AdBase):
    pass


class Ad(AdBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    user_id: UUID4


class AdTitle(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    ad_number: int
