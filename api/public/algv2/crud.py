from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select, text

from api.pg_database import get_session
from api.public.algv2.pg_models import Contact, School, Message, Course, Group, Booking


class AbsCRUD:
    _model = None

    @classmethod
    def create_instance(cls, instance: dict, db: Session = Depends(get_session)):
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def read_instancies(cls, offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
        contacts = db.exec(select(cls._model).offset(offset).limit(limit)).all()
        return contacts

    @classmethod
    def read_instance(cls, instance_id: int, db: Session = Depends(get_session)):
        contact = db.get(cls._model, instance_id)
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{cls._model.__name__} not found with id: {instance_id}",
            )
        return contact

    @classmethod
    def update_instance(cls, instance_id: int, instance: dict, db: Session = Depends(get_session)):
        instance_to_update = db.get(cls._model, instance_id)
        if not instance_to_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{cls._model.__name__} not found with id: {instance_id}",
            )
        for key, value in instance.items():
            setattr(instance_to_update, key, value)
        db.add(instance_to_update)
        db.commit()
        db.refresh(instance_to_update)
        return instance_to_update

    @classmethod
    def delete_instance(cls, instance_id: int, db: Session = Depends(get_session)):
        instance = db.get(cls._model, instance_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{cls._model.__name__} not found with id: {instance_id}",
            )
        db.delete(instance)
        db.commit()
        return {"ok": True}


class ContactCRUD(AbsCRUD):
    _model = Contact

class MessageCRUD(AbsCRUD):
    _model = Message