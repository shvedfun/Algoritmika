from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from api.pg_database import get_session
from api.public.alg.models import Contact, ContactUpdate, Message


def create_contact(contact: Contact, db: Session = Depends(get_session)):
    contact_to_db = Contact.model_validate(contact)
    db.add(contact_to_db)
    db.commit()
    db.refresh(contact_to_db)
    return contact_to_db


def create_message(message: Message, db: Session = Depends(get_session)):
    message_to_db = Message.model_validate(message)
    db.add(message_to_db)
    db.commit()
    db.refresh(message_to_db)
    return message_to_db


def read_contacts(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    contacts = db.exec(select(Contact).offset(offset).limit(limit)).all()
    return contacts


def read_contact(contact_id: int, db: Session = Depends(get_session)):
    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact not found with id: {contact_id}",
        )
    return contact


def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_session)):
    contact_to_update = db.get(Contact, contact_id)
    if not contact_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero not found with id: {contact_id}",
        )

    contact_data = contact.model_dump(exclude_unset=True)
    for key, value in contact_data.items():
        setattr(contact_to_update, key, value)

    db.add(contact_to_update)
    db.commit()
    db.refresh(contact_to_update)
    return contact_to_update


# def delete_hero(hero_id: int, db: Session = Depends(get_session)):
#     hero = db.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Hero not found with id: {hero_id}",
#         )
#
#     db.delete(hero)
#     db.commit()
#     return {"ok": True}
