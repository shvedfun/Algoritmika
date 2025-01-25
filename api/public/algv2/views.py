import datetime
import http.client
import traceback
from uuid import UUID, uuid4
from typing import Union
from fastapi import APIRouter, Depends, Query, Request, Form, BackgroundTasks, HTTPException, Response
from sqlmodel import Session, select, desc
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from api.ydb_utils import db, db_executor
from api.utils.logger import get_logger
from api.public.algv2.models import Contact, Student, StudentStatus, School, Course, Group, \
    Message, FAQ, Booking, BookingStatusEnum, UpdateContactStatus
from api.utils.messages_utils import MessagesUtils
from amo_utils.client import AMOClient
from api.config import settings, partners

router = APIRouter()

logger = get_logger(__name__)

def delete_null(r: dict):
    for k, v in r.copy().items():
        if v is None:
            r.pop(k)
    return r

def test_back_task():
    pass

@router.post("/message", response_model=Message)
def create_message(ms: Message, background_tasks: BackgroundTasks): #
    logger.debug(f'handle message from ai {ms}')
    background_tasks.add_task(MessagesUtils.handle_message_from_ai, [ms,])
    return ms


# @router.post("/contact_status", response_model=StudentStatus)
# def create_contact_status(contact_status: StudentStatus):
#     # todo add logics
#     return contact_status

@router.get("/student", response_model=list[Student])
def get_students(contact_id: int = None):
    sql = 'SELECT * FROM i_student'
    if contact_id:
        sql += f' WHERE contact_id = {contact_id}'
    # sql += ' ORDER BY id'
    result = db.execute_query(sql)[0].rows
    results = []
    for r in result:
        r = delete_null(r)
        results.append(Student(**r))
    return results


@router.post("/student", response_model=Student)
def post_students(student: Student):
    try:
        student.id = student.id or uuid4()
        student.updated = datetime.datetime.utcnow().isoformat()
        sql = f'UPSERT INTO i_student (id, first_name, last_name, middle_name, age, school_id, course_id, group_id, contact_id, updated) ' \
              f"VALUES (\'{student.id}\', \'{student.first_name}\', \'{student.last_name}\', \'{student.middle_name}\'," \
              f"{student.age}, {student.school_id}, {student.course_id}, {student.group_id}, {student.contact_id}, CAST(\'{student.updated}\' AS DateTime))"
        logger.debug(f'sql = {sql}')
        result = db.execute_query(sql)
        sql = f'SELECT * FROM i_student WHERE id = \'{student.id}\''
        st = db.execute_query(sql)[0].rows[0]
        logger.info(f'st = {st}')
        st = delete_null(st)
        student = Student(**st)
        logger.debug(f'result = {student}')
    except Exception as e:
        logger.error(f'Error = {traceback.format_exc()}')
    return student


@router.patch("/student/{id}", response_model=Student)
def patch_students(id: str, student: Student):
    student = student.model_dump()
    del student['id']
    student["updated"] = datetime.datetime.utcnow()
    student = delete_null(student)
    sql = f"UPDATE i_student SET "
    adds = []
    for k, v in student.items():
        add_sql = ''
        add_sql += ' ' + k + ' = '
        if type(v) in (int, float):
            add_sql += str(v)
        elif type(v) in (datetime.datetime,):
            add_sql += f'Cast(\'{v.isoformat()}\' AS DateTime)'
        else:
            add_sql += f'\'{str(v)}\''
        adds.append(add_sql)
    sql += ','.join(adds)
    sql += f' WHERE id = \'{id}\''
    logger.debug(f'sql = {sql}')
    result = db.execute_query(sql)
    sql = f'SELECT * FROM i_student WHERE id = \'{id}\''
    st = db.execute_query(sql)[0].rows[0]
    logger.info(f'st = {st}')
    st = delete_null(st)
    student = Student(**st)
    logger.debug(f'result = {student}')
    return student


@router.get('/booking', response_model=list[Booking])
def get_booking(student_id: str = None, group_id: int = None):
    result = db_executor.get_booking(student_id, group_id)
    results = []
    for r in result:
        r = delete_null(r)
        results.append(Booking(**r))
    return results


@router.post("/booking", response_model=Union[Booking, dict])
async def new_booking(bk: Booking, response: Response):
    amo_client = AMOClient(url_prefix= settings.AMO_URL, long_token= settings.AMO_TOKEN,)
    # exists_capacity = get_group_capacity_exists(group_id)
    tst = datetime.datetime.utcnow().replace(microsecond=0, tzinfo=None)
    if not bk.created:
        bk.created = tst
    bk.updated = tst
    group = db_executor.get_group(bk.group_id)
    logger.debug(f'group = {group}')
    if not group:
        response.status_code = http.client.NOT_ACCEPTABLE
        return bk
    n_book = db_executor.get_number_booking(bk.group_id)
    logger.debug(f'n_book = {n_book}')
    if n_book < group.get('capacity', -1):
        bk.status = BookingStatusEnum.ok
    else:
        response.status_code = http.client.NOT_ACCEPTABLE
        bk.status = BookingStatusEnum.rjct
        return bk
    db_executor.upsert_booking(bk)
    lead_id = db_executor.get_lead_id_from_student_id(bk.student_id)
    if lead_id:
        await amo_client.lead_done(lead_id)
    return bk

# @router.patch("/booking", response_model=Union[Booking, dict])
# def patch_booking(bk: Booking, response: Response):
#     # exists_capacity = get_group_capacity_exists(group_id)
#     tst = datetime.datetime.utcnow().replace(microsecond=0, tzinfo=None)
#     if not bk.created:
#         bk.created = tst
#     bk.updated = tst
#     group = db_connector.get_group(bk.group_id)
#     logger.debug(f'group = {group}')
#     sql = f'UPDATE INTO i_booking (student_id, group_id, status, created, updated) VAlUES ' \
#         f'(\'{bk.student_id}\', {bk.group_id}, \'{bk.status}\'' \
#           f', CAST(\'{bk.created.isoformat()}\' AS DateTime), CAST(\'{bk.updated.isoformat()}\' AS DateTime))'
#     logger.debug(f'sql = {sql}')
#     db.execute_query(sql)
#     return bk


@router.get("/contact", response_model=list[Contact])
def get_contacts(contact_id: int = None):
    result = db_executor.get_contact(contact_id)
    logger.debug(f'result = {result}')
    results = []
    for r in [result] if result else []:
        r = delete_null(r)
        results.append(Contact(**r))
    return results


@router.get("/school", response_model=list[School])
def get_school():
    get_course_sql = 'SELECT * FROM i_school'
    result = db.execute_query(get_course_sql)[0].rows
    results = []
    for r in result:
        r = delete_null(r)
        results.append(School(**r))
    return results


@router.get("/course", response_model=list[Course])
def get_course(school_id: int = None):
    get_course_sql = 'SELECT c.* FROM i_course AS c'
    if school_id is not None:
        get_course_sql += f' JOIN i_group AS g ON g.course_id = c.id WHERE g.school_id = {school_id}'
    result = db.execute_query(get_course_sql)[0].rows
    results = []
    for r in result:
        r['properties'] = {
            "properties": r.get("properties", ""),
            "summary": r.get("summary", ""),
            "result": r.get("result", ""),
            "cases_full_description": r.get("cases_full_description", ""),
            "presentation_link": r.get("presentation_link", ""),
            "cases": r.get("cases", "")
        }
        results.append(Course(**r))
    # todo add logics
    return results


@router.get("/group", response_model=list[Group])
def get_group(school_id: int, course_id: int = None):
    get_course_sql = f'SELECT * FROM i_group WHERE school_id = {school_id}'
    if course_id is not None:
        get_course_sql += f' AND course_id = {course_id}'

    result = db.execute_query(get_course_sql)[0].rows
    results = []
    for r in result:
        results.append(Group(**r))
    return result

@router.get("/faq", response_model=list[FAQ])
def get_faq(school_id: int = None):
    sql = f'SELECT * FROM i_faq'
    result = db.execute_query(sql)[0].rows
    results = []
    for r in result:
        results.append(FAQ(**r))
    return result

@router.post("/update_contact_status", response_model=dict)
async def update_contact_status(data: UpdateContactStatus):
    logger.debug('update_contact_status get data = %r', data)
    result = {}
    contact = db_executor.get_contact(contact_id=data.contact_id)
    lead_id = None
    partner = None
    if contact:
        lead_id = contact.get('amo_lead_id')
        partner = contact.get('partner')
    # lead_id = db_executor.get_lead_id_from_contact_id(data.contact_id)
    if lead_id and partner:
        try:
            pipelines = settings.partners[partner]["pipelines"]
            pipelines_statuses = settings.partners[partner]["pipelines_statuses"]
            amo_client = AMOClient(
                url_prefix=settings.partners[partner]["AMO_URL"],
                long_token=settings.partners[partner]["AMO_TOKEN"],
                pipelines=pipelines,
                pipelines_statuses=pipelines_statuses
            )
            result = await amo_client.update_lead_status(lead_id, data.status)
            logger.debug(f'result = {result}')
        except Exception as e:
            logger.error('update_contact_status error = %r', str(e))
            raise HTTPException(status_code=400, detail=f'{e} parameters = {data}')
    else:
        logger.warning(
            "update_contact_status: contact, lead or partner is None. Contact = %r, lead_id = %r, partner = %r",
            contact, lead_id, partner
        )
        raise HTTPException(status_code=400, detail=f"lead or partner not fount by contact id = {data.contact_id}")
    return result
