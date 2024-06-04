import datetime
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Query, Request, Form, BackgroundTasks
from sqlmodel import Session, select, desc
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from api.db_utils import db
from api.utils.logger import logger_config
from api.public.algv2.models import Contact, Student, StudentStatus, School, Course, Group, Message, FAQ, Booking

router = APIRouter()

logger = logger_config(__name__)

def delete_null(r: dict):
    for k, v in r.copy().items():
        if v is None:
            r.pop(k)
    return r

def test_back_task():
    pass

@router.post("/message", response_model=Message)
def create_message(ms: Message, back_task: BackgroundTasks=None): #
    ms.id = str(uuid4())
    # ms.created = datetime.datetime.now(tz=datetime.timezone.utc)
    sql = f'INSERT INTO i_message (id, text, ai_id, contact_id, created) VALUES (\'{ms.id}\', \'{ms.text}\', \'{ms.ai_id}\', {ms.contact_id}, CAST(\'{ms.created.isoformat()}\' AS Timestamp))'
    result = db.execute_query(sql)
    sql = f'SELECT * FROM i_message WHERE id = \'{ms.id}\''
    result = db.execute_query(sql)[0].rows[0]
    result['created'] = datetime.datetime.fromtimestamp(result['created']/10**6)
    result = Message(**result)
    return result # RedirectResponse("/message/html")


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
    sql = 'SELECT * FROM i_booking'
    result = db.execute_query(sql)[0].rows
    results = []
    for r in result:
        r = delete_null(r)
        results.append(Booking(**r))
    return results

@router.post("/booking", response_model=Booking)
def new_booking(bk: Booking):
    # exists_capacity = get_group_capacity_exists(group_id)
    tst = datetime.datetime.utcnow().replace(microsecond=0, tzinfo=None)
    if not bk.created:
        bk.created = tst
    bk.updated = tst
    sql = f'UPSERT INTO i_booking (student_id, group_id, status, created, updated) VAlUES ' \
        f'(\'{bk.student_id}\', {bk.group_id}, \'{bk.status}\'' \
          f', CAST(\'{bk.created.isoformat()}\' AS DateTime), CAST(\'{bk.updated.isoformat()}\' AS DateTime))'
    logger.debug(f'sql = {sql}')
    db.execute_query(sql)
    return bk


@router.get("/contact", response_model=list[Contact])
def get_contacts():
    sql = 'SELECT * FROM i_contact'
    # sql += ' ORDER BY "id"'
    result = db.execute_query(sql)[0].rows
    logger.debug(f'result = {result}')
    results = []
    for r in result:
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
