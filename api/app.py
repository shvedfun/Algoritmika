import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.config import Settings
# from api.database import create_db_and_tables
from api.public import api as public_api
from api.utils.logger import get_logger
from api.ydb_utils import DBProvider
from api.ydatabase4del import create_tables
from fastapi.middleware.cors import CORSMiddleware
from api.background import BackgroundManager

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DBProvider()
    result = db.execute_query('select 1')
    logger.info(f'result = {result[0].rows}')
    create_tables(db)
    background_manager = BackgroundManager()
    asyncio.create_task(background_manager.run())
    logger.info("startup: triggered")
    yield
    logger.info("shutdown: triggered")


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        lifespan=lifespan,
    )

    app.include_router(public_api)

    return app
