from datetime import datetime
from typing import List, Optional
from sqlalchemy import Table, Column, Integer, String, ForeignKey, JSON, MetaData, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from api.pg_database import Base
from api.config import settings
from api.utils.logger import get_logger
from api.pg_database import async_engine #sync_engine,

logger = get_logger(__name__)

class School(Base):
    __tablename__ = "alg_school"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(100))

    groups: Mapped[List["Group"]] = relationship(back_populates="school", cascade="all, delete-orphan",)


class Course(Base):
    __tablename__ = "alg_course"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String[100], name="Курс")
    description: Mapped[str] = mapped_column(String)
    age_from: Mapped[int] = mapped_column(Integer)
    age_to: Mapped[int] = mapped_column(Integer)
    properties: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(String)
    result: Mapped[str] = mapped_column(String)
    cases_full_description: Mapped[str] = mapped_column(String)
    presentation_link: Mapped[str] = mapped_column(String)
    cases: Mapped[str] = mapped_column(String)

    groups: Mapped[List["Group"]] = relationship(back_populates="course", cascade="all, delete-orphan",)


class Faq(Base):
    __tablename__ = "alg_faq"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String)
    answer: Mapped[str] = mapped_column(String)
    school_id: Mapped[int] = mapped_column(Integer)


class Group(Base):
    __tablename__ = "alg_group"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    school_id: Mapped[int] = mapped_column(ForeignKey(School.id))
    school: Mapped[School] = relationship(back_populates="groups")
    course_id: Mapped[int] = mapped_column(ForeignKey(Course.id))
    course: Mapped[Course] = relationship(back_populates="groups")
    teacher: Mapped[str] = mapped_column(String[100])
    schedule: Mapped[str] = mapped_column(String)
    capacity: Mapped[int] = mapped_column(Integer,)


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


class Student(Base):
    __tablename__ = "alg_student"

    id: Mapped[str] = mapped_column(String[64], primary_key=True)
    first_name: Mapped[str] = mapped_column(String[100])
    last_name: Mapped[str] = mapped_column(String[100])
    middle_name: Mapped[str] = mapped_column(String[100])
    age: Mapped[int] = mapped_column(Integer)
    contact_id: Mapped[int] = mapped_column(ForeignKey(Contact.id))


class Booking(Base):
    __tablename__ = "alg_booking"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(ForeignKey(Student.id))
    group_id: Mapped[int] = mapped_column(ForeignKey(Group.id))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())



def create_db_and_tables():
    logger.debug(f'Создаю базу')
    # Base.metadata.create_all(sync_engine)