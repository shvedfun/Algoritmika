from datetime import datetime, timezone
from pydantic import BaseModel
from enum import Enum, IntEnum
from uuid import uuid4


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
    amo_lead_id: int | None = None
    updated: datetime | None = None
    created: datetime = None
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone: str
    email: str = None
    params: dict | None = None
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
    properties: dict = {}


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
    contact_id: int | None = None
    student_id: str | None = None
    group_id: int
    status: str = None
    trial: bool = True
    created: datetime = None
    updated: datetime = None
    embedded: dict | None = None


class Message(BaseModel):
    id: str | None = str(uuid4())
    text: str
    ai_id: str | None
    created: datetime = datetime.now(tz=timezone.utc)
    contact_id: int

class PhoneMessage(BaseModel):
    text: str
    created: datetime
    phone: str

class FAQ(BaseModel):
    id: int | None
    question: str
    answer: str
    school_id: int | None = None

class WhatCrmMessage(BaseModel):
    message: dict = None

    def get_phone(self):
        return "1234567890"

    def get_text(self):
        return "Проверочный текст"


class UpdateContactStatus(BaseModel):
    contact_id: int
    status: int
    detail: dict