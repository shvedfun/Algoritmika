from fastapi import APIRouter, Depends, Query, Request, Form, BackgroundTasks
from sqlmodel import Session, select, desc
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from api.pg_database import get_session
from api.public.alg.crud import (
    create_contact,
    # delete_contact,
    read_contact,
    read_contacts,
    update_contact,
    create_message,
)
from api.public.alg.models import ContactCreate, ContactRead, ContactUpdate, ContactBase, Contact, Message


router = APIRouter()
# router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@router.post("/contact/form", response_model=ContactRead)
def create_a_contact(con_name: str = Form(), con_phone: str = Form(), db: Session = Depends(get_session)):
    contact = ContactBase(name=con_name, phone=con_phone)
    return create_contact(contact=contact, db=db)


def test_back_task(message: Message):
    print(f'message = {message}')


@router.post("/message/form", response_model=Message)
def create_a_message(mess_text: str = Form(), contact_id: int=Form(), db: Session = Depends(get_session), back_task: BackgroundTasks=None): #
    message = Message(text=mess_text, contact_id=contact_id)
    result = create_message(message=message, db=db)
    back_task.add_task(test_back_task, result)
    return result # RedirectResponse("/message/html")


@router.post("/contact", response_model=ContactRead)
def create_a_contact(contact: ContactCreate, db: Session = Depends(get_session)):
    return create_contact(contact=contact, db=db)


@router.get("/contact", response_model=list[ContactRead])
def get_contactes(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    return read_contacts(offset=offset, limit=limit, db=db)


@router.get("/contact/{contact_id}", response_model=ContactRead)
def get_a_contact(contact_id: int, db: Session = Depends(get_session)):
    return read_contact(contact_id=contact_id, db=db)


@router.get("/contact/{contact_id}/html", response_class=HTMLResponse)
def get_a_contact_html(request: Request, contact_id: int, db: Session = Depends(get_session)):
    contact =  read_contact(contact_id=contact_id, db=db)
    print(f'contact = {contact.dict()}')
    contacts_sql = select(Contact)
    contacts = db.exec(contacts_sql)
    return templates.TemplateResponse(
        request=request,
        name='contact.html',
        context={"contact": contact, "id": contact_id, "results": contacts},
    )


@router.get("/message/html", response_class=HTMLResponse)
def get_messages(
        request:Request, offset: int = 0, limit: int = Query(default=100, lte=100), db: Session = Depends(get_session),
):
    messages = db.exec(select(Message, Contact).join(Contact).offset(offset).limit(limit).order_by(desc(Message.id))).all()
    contacts = db.exec(select(Contact)).fetchall()
    return templates.TemplateResponse(
        request=request, name="messages.html", context={"messages": messages, "contacts": contacts}
    )


@router.patch("/contact/{contact_id}", response_model=ContactRead)
def update_a_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_session)):
    return update_contact(contact_id=contact_id, contact=contact, db=db)


# @router.delete("/{contact_id}")
# def delete_a_contact(contact_id: int, db: Session = Depends(get_session)):
#     return delete_contact(contact_id=contact_id, db=db)
