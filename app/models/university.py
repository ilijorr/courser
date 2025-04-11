from sqlmodel import Field, SQLModel

from models import register_model

@register_model
class University(SQLModel, table = True):
    id: int | None = Field(
            default=None,
            primary_key=True,
            index=True
            )
    name: str = Field(...)
