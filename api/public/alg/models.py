from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel, Column, CheckConstraint, TIMESTAMP, ForeignKey
import sqlalchemy as sa

from api.public.team.models import Team
from api.utils.generic_models import HeroTeamLink


class ContactBase(SQLModel):
    name: str = Field()
    phone: str = Field(sa_type=sa.CHAR(length=10))


class Contact(ContactBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        nullable=False,
        sa_column_kwargs={"server_default": sa.func.now()}
    )
    updated: datetime| None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"onupdate": sa.func.now(), "server_default": sa.func.now()}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Super Man",
                "phone": "Clark Kent",
                "cteated": '2024-04-01 00:00:00',
                "updated": '2024-04-01 00:00:00',
            }
        }


class ContactCreate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int
    name: str | None = None


class ContactUpdate(ContactBase):
    name: str | None = None
    phone: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Super Man",
                "phone": "0000000000",
            }
        }


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str | None
    ai_id: int | None
    created: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        nullable=False,
        sa_column_kwargs={"server_default": sa.func.now()}
    )
    contact_id: int | None = Field(default=None, foreign_key='contact.id')

