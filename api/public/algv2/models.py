from datetime import datetime, timezone
from pydantic import BaseModel
from enum import Enum, IntEnum
from uuid import UUID


class ContactStatusEnum(str, Enum):
    cold = 'cold' #first contact
    wip_ai = 'wip_ai'
    cancel = 'cncl'
    done = 'done'


class Student(BaseModel):
    id: str
    updated: datetime | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    age: int | None = None
    school_id: int | None = None
    course_id: int | None = None
    group_id: int | None = None
    contact_id: int


class Contact(BaseModel):
    id: int | None
    amo_id: int | None = None
    updated: datetime | None = None
    created: datetime = None
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone: str
    email: str = None
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
    age_from: int | None
    age_to: int | None


class Group(BaseModel):
    id: int | None
    course_id: int
    school_id: int
    schedule: str
    teacher: str
    capacity: int

class BookingStatusEnum(str, Enum):
    ok = 'ok' #first contact
    rjct = 'reject_full'
    wait = 'wait'


class Booking(BaseModel):
    student_id: str
    group_id: int
    status: str = None
    trial: bool = True
    created: datetime = None
    updated: datetime = None


class Message(BaseModel):
    id: str | None
    text: str
    ai_id: str | None
    created: datetime
    contact_id: int


class FAQ(BaseModel):
    id: int | None
    question: str
    answer: str
    school_id: int | None = None
