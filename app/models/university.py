from typing import List
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from models import register_model
from enums.university import Country

@register_model
class University(SQLModel, table = True):
    id: int | None = Field(
            default=None,
            primary_key=True,
            index=True
            )
    name: str = Field(...)
    country: Country = Field(
            nullable=False
            )
    courses: List["Course"] = Relationship(
            back_populates="university",
            cascade_delete=True
            )

    @field_validator('country', mode='before')
    @classmethod
    def validate_country(cls, v):
        if isinstance(v, str):
            try:
                return Country(v.upper())
            except ValueError:
                raise ValueError(f"invalid country string, expected name of country but got {v}")
        elif isinstance(v, Country):
            return v
        raise TypeError(f"expected country or string, got {type(v)}")
