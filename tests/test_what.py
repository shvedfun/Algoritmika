from api.public.algv2.models import Contact, ContactStatusEnum
import pytest
from contextlib import nullcontext
from api.utils.logger import get_logger
from api.config import settings

logger = get_logger(__name__)

@pytest.fixture(scope="function", autouse=True)
def prepare_db():
    # assert settings.MODE == "TEST"
    logger.debug('Я в prepare_db')
    yield
    logger.debug('Я закончил') #rollback

@pytest.fixture
def contacts():
    contacts = [
        Contact(id=1, phone="phone"),
        Contact(id=2, phone="phone2"),

    ]
    return contacts

@pytest.fixture
def delete_contacts():
    #Удалить контакт
    logger.debug(f'Удаляю что-то в тесте')


@pytest.mark.usefixtures("delete_contacts")
class TestModels:
    def test_main(self, contacts):
        assert 1 == 1

    @pytest.mark.parametrize(
        "id, phone, expectation",
        [
            (1, "123456", nullcontext()),
            (2, "334444", nullcontext()) #pytest.raises(TypeError)
        ]
    )
    def test_contact(self, id, phone, expectation):
        with expectation:
            contact = Contact(id=id, phone=phone)
            assert contact.phone == phone
            assert contact.status == ContactStatusEnum.cold
