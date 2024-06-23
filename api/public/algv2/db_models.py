from typing import List, Optional
from sqlalchemy import Table, Column, Integer, String, ForeignKey, JSON, MetaData, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from api.database import Base
from api.config import settings
from api.utils.logger import get_logger
from api.database import sync_engine

logger = get_logger(__name__)

class Contact(Base):
    __tablename__ = "alg_contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String[10],)
    messages: Mapped[List["Message"]] = relationship(back_populates="contact", cascade="all, delete-orphan",)

    def __repr__(self) -> str:
        return f'{self.name} ({str(self.id)})'


class Message(Base):
    __tablename__ = "alg_message"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("alg_contact.id"))
    text: Mapped[str] = mapped_column(Text())

    contact: Mapped["Contact"] = relationship(back_populates="messages")


def create_db_and_tables():
    logger.debug(f'Создаю базу')

    Base.metadata.create_all(sync_engine)