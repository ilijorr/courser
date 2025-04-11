from sqlmodel import Field, SQLModel, String

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
            sa_type=String,
            nullable=False
            )
