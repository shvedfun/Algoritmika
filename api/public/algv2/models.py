from datetime import datetime, timezone
from pydantic import BaseModel
from enum import Enum, IntEnum
from uuid import UUID


class ContactStatusEnum(str, Enum):
    cold = 'cold'
    wip_ai = 'wip_ai'
    cancel = 'cncl'
    done = 'done'


class Student(BaseModel):
    id: str
    updated: datetime
    first_name: str
    last_name: str
    middle_name: str
    age: int
    school: int
    course_id: int
    group_id: int


class Contact(BaseModel):
    id: int | None
    updated: datetime
    first_name: str
    last_name: str
    middle_name: str
    telephone: str
    email: str
    status: ContactStatusEnum = ContactStatusEnum.cold


class StudentStatus(BaseModel):
    id: int | None
    student_id: int
    status: int
    created: datetime
    ai_id: int


class School(BaseModel):
    id: int | None = None
    number: int
    name: str


class Course(BaseModel):
    id: int | None
    name: str
    description: str


class Group(BaseModel):
    id: int | None
    course_id: int
    school_id: int
    schedule: str
    teacher: str
    capacity: int


class Message(BaseModel):
    id: str | None
    text: str
    ai_id: str | None
    created: datetime
    contact_id: int

