from typing import Any
from fastapi import Depends, HTTPException, status
# from sqlmodel import Session, select, text

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, insert, update, delete, text
from sqlalchemy.sql.expression import func
from api.pg_database import get_async_session, async_engine, sync_engine, get_session
from api.public.algv2.pg_models import Contact, School, Message, Course, Group, Booking
from api.utils.logger import get_logger


logger = get_logger(__name__)


class AbsCRUD:
    _model = None

    @classmethod
    def upsert_instance(cls, instance: dict):
        with sync_engine.connect() as conn:
            stmt = insert(cls._model).returning(cls._model)
            logger.debug(f'instance = {instance}')
            instance = conn.execute(stmt, [instance]).fetchone()
            conn.commit()
            return instance

    @classmethod
    def read_instancies(cls, offset: int = 0, limit: int = 20): #, db: AsyncSession = Depends(get_session)
        with sync_engine.connect() as conn:
            stmt = select(cls._model).offset(offset).limit(limit).order_by(cls._model.id) #.order_by(cls._model.id)
            logger.debug(f'stmt = {stmt}')
            result = conn.execute(stmt)
            logger.debug(f'result = {result}')
            #db.get(cls._model).offset(offset).limit(limit).all()
            return result

    @classmethod
    def read_instance(cls, instance_id: int) -> Any:
        with sync_engine.connect() as conn:
            stmt = select(cls._model).filter(cls._model.id == instance_id)
            result = conn.execute(stmt)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{cls._model.__name__} not found with id: {instance_id}",
                )
            return result

    @classmethod
    def update_instance(cls, instance_id: int, instance: dict):
        with sync_engine.connect() as conn:
            stmt = update(cls._model).returning(cls._model).where(cls._model.id == instance_id).values(**instance)
            instance = conn.execute(stmt).fetchone()
            conn.commit()
            logger.debug(f'instance = {instance}')
            return instance

    @classmethod
    def delete_instance(cls, instance_id: int):
        with sync_engine.connect() as conn:
            stmt = delete(cls._model).returning(cls._model).where(cls._model.id == instance_id)
            instance = conn.execute(stmt).fetchone()
            if not instance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{cls._model.__name__} not found with id: {instance_id}",
                )
            conn.commit()
            return {"ok": True}

    @classmethod
    def count(cls, filters={}):
        with sync_engine.connect() as conn:
            stmt = select(cls._model)
            if filters:
                stmt = cls._add_filters(stmt, filters)
            stmt = stmt.with_only_columns(func.count(cls._model.id))
            result = conn.execute(stmt).scalar_one()
            logger.debug(f'result = {result}')
            return result

    @classmethod
    def _add_filters(cls, stmt, filters: dict):
        for k, v in filters.items():
            pass    #TODO add filters to stmt
        return stmt

class ContactCRUD(AbsCRUD):
    _model = Contact


class MessageCRUD(AbsCRUD):
    _model = Message


class SchoolCRUD(AbsCRUD):
    _model = School


class CourseCRUD(AbsCRUD):
    _model = Course


class GroupCRUD(AbsCRUD):
    _model = Group



# class AsyncAbsCRUD:
#     _model = None
#
#     @classmethod
#     def create_instance(cls, instance: dict, db: AsyncSession = Depends(get_async_session())):
#         db.add(instance)
#         db.commit()
#         db.refresh(instance)
#         return instance
#
#     @classmethod
#     async def read_instancies(cls, offset: int = 0, limit: int = 20): #, db: AsyncSession = Depends(get_session)
#         async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
#         logger.debug(f'async_session = {async_session}')
#         # async with async_session() as conn:
#         async with async_engine.connect() as conn:
#             stmt = select(cls._model) #.order_by(cls._model.id)
#             logger.debug(f'stmt = {stmt}')
#             result = await conn.execute(text('select 1'))
#             logger.debug(f'result = {result}')
#             result = result.scalars()
#             #db.get(cls._model).offset(offset).limit(limit).all()
#         return result
#
#     @classmethod
#     def read_shools(cls):
#         with sync_engine.connect() as conn:
#             stmt = select(School)
#             result = conn.execute(stmt)
#             logger.debug(f'result = {result}')
#         return result
#
#     @classmethod
#     def read_instance(cls, instance_id: int, db: AsyncSession = Depends(get_async_session)):
#         contact = db.get(cls._model, instance_id)
#         if not contact:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"{cls._model.__name__} not found with id: {instance_id}",
#             )
#         return contact
#
#     @classmethod
#     def update_instance(cls, instance_id: int, instance: dict, db: AsyncSession = Depends(get_async_session)):
#         instance_to_update = db.get(cls._model, instance_id)
#         if not instance_to_update:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"{cls._model.__name__} not found with id: {instance_id}",
#             )
#         for key, value in instance.items():
#             setattr(instance_to_update, key, value)
#         db.add(instance_to_update)
#         db.commit()
#         db.refresh(instance_to_update)
#         return instance_to_update
#
#     @classmethod
#     def delete_instance(cls, instance_id: int, db: AsyncSession = Depends(get_async_session)):
#         instance = db.get(cls._model, instance_id)
#         if not instance:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"{cls._model.__name__} not found with id: {instance_id}",
#             )
#         db.delete(instance)
#         db.commit()
#         return {"ok": True}
