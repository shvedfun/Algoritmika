import datetime
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Query, Request, Form, BackgroundTasks
from sqlmodel import Session, select, desc
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from api.db_utils import db

from api.public.algv2.models import StudentStatus, School, Course, Group, Message

router = APIRouter()

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


@router.post("/contact_status", response_model=StudentStatus)
def create_contact_status(contact_status: StudentStatus):
    # todo add logics
    return contact_status


@router.get("/school", response_model=list[School])
def get_school():
    get_course_sql = 'SELECT * FROM i_school'
    result = db.execute_query(get_course_sql)[0].rows
    results = []
    for r in result:
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

# @router.post("/contact", response_model=ContactRead)
# def create_a_contact(contact: ContactCreate, db: Session = Depends(get_session)):
#     return create_contact(contact=contact, db=db)
#
#
# @router.get("/contact", response_model=list[ContactRead])
# def get_contactes(
#     offset: int = 0,
#     limit: int = Query(default=100, lte=100),
#     db: Session = Depends(get_session),
# ):
#     return read_contacts(offset=offset, limit=limit, db=db)
#
#
# @router.get("/contact/{contact_id}", response_model=ContactRead)
# def get_a_contact(contact_id: int, db: Session = Depends(get_session)):
#     return read_contact(contact_id=contact_id, db=db)
#
#
# @router.get("/contact/{contact_id}/html", response_class=HTMLResponse)
# def get_a_contact_html(request: Request, contact_id: int, db: Session = Depends(get_session)):
#     contact =  read_contact(contact_id=contact_id, db=db)
#     print(f'contact = {contact.dict()}')
#     contacts_sql = select(Contact)
#     contacts = db.exec(contacts_sql)
#     return templates.TemplateResponse(
#         request=request,
#         name='contact.html',
#         context={"contact": contact, "id": contact_id, "results": contacts},
#     )
#
#
# @router.get("/message/html", response_class=HTMLResponse)
# def get_messages(
#         request:Request, offset: int = 0, limit: int = Query(default=100, lte=100), db: Session = Depends(get_session),
# ):
#     messages = db.exec(select(Message, Contact).join(Contact).offset(offset).limit(limit).order_by(desc(Message.id))).all()
#     contacts = db.exec(select(Contact)).fetchall()
#     return templates.TemplateResponse(
#         request=request, name="messages.html", context={"messages": messages, "contacts": contacts}
#     )
#
#
# @router.patch("/contact/{contact_id}", response_model=ContactRead)
# def update_a_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_session)):
#     return update_contact(contact_id=contact_id, contact=contact, db=db)
#

# @router.delete("/{contact_id}")
# def delete_a_contact(contact_id: int, db: Session = Depends(get_session)):
#     return delete_contact(contact_id=contact_id, db=db)
