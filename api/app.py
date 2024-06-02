import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.config import Settings
# from api.database import create_db_and_tables
from api.public import api as public_api
from api.utils.logger import logger_config
from api.utils.mock_data_generator import create_heroes_and_teams
from api.db_utils import DBProvider
from api.ydatabase import create_tables
from fastapi.middleware.cors import CORSMiddleware
from api.background import BackgroundManager

logger = logger_config(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create_db_and_tables()
    # create_heroes_and_teams()
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
        # docs_url="/docs",
        description=settings.DESCRIPTION,
        lifespan=lifespan,
    )

    # origins = ["*"]
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=origins,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"]
    # )

    app.include_router(public_api)

    return app
