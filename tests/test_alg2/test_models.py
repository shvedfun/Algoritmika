import pytest
from contextlib import nullcontext as does_not_raise
from sqlalchemy import insert, update, select, delete
from sqlalchemy.orm import Session
from api.public.algv2 import pg_models
from api.pg_database import sync_engine
from api.utils.logger import get_logger
from api.public.algv2.pg_models import Base, Contact, sync_engine
from api.config import settings


logger = get_logger(__name__)

@pytest.fixture
def contacts():
    contacts = [
        {"name": "Иван", "phone": "0987654321"},
        {"name": "Петр", "phone": "79871234567"}
    ]


@pytest.fixture
def empty_contacts():
    pass

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    assert settings.MODE == "TEST"
    Base.metadata.create_all(sync_engine)
    yield
    Base.metadata.drop_all(sync_engine)
    logger.debug(f'')


# @pytest.mark.parametrize(
#     "name, phone, result, result2",
#     [
#         ("Иван", "0987654321", False, pytest.raises(ValueError)),
#         ("Петр", "79871234567", True, does_not_raise()),
#     ]
# )
@pytest.mark.usefixtures("empty_contacts")
class TestContacts:
    def test_contact(self, contacts, ):
        with Session(sync_engine) as session:
            for contact in contacts:
                contact = db_models.Contact(**contact)
                session.add(contact)
                logger.debug(f'contact = {contact}')
            session.commit()



