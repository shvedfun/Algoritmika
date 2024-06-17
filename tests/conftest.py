import pytest
from api.utils.logger import get_logger
from api.config import settings

logger = get_logger(__name__)

@pytest.fixture(scope="function", autouse=True)
def prepare_db():
    # assert settings.MODE == "TEST"
    logger.debug('Я в prepare_db')
    yield
    logger.debug('Я закончил') #rollback