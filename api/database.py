import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from api.config import settings
from api.utils.logger import get_logger

logger = get_logger(__name__)


connect_args = {"check_same_thread": False}

sync_engine = create_engine(
    url=settings.DATABASE_URI_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)


async_engine = create_async_engine(
    url=settings.DATABASE_URI_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)


async def get_session():
    async with AsyncSession(async_engine) as session:
        yield session


async def get_db_version():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        logger.debug(f'res = {res.all()}')


class Base(DeclarativeBase):
    pass

if settings.IS_LOCAL:
    session_factory = sessionmaker(sync_engine)
    async_session_factory = async_sessionmaker(async_engine)

    asyncio.run(get_db_version())







