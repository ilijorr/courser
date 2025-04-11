from pydantic import BaseModel, ConfigDict, Field

from enums.university import Country

class UniversityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=256,
                      examples=["University of Novi Sad", "University of Belgrade"])
    country: Country = Field(...,
                             examples=[Country.SERBIA])

class UniversityResponse(UniversityCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., ge=1)
