import json
import logging

import pytest
from api.utils.logger import get_logger
from api.wazzup.wazzup_utils import WazzupUtils

logger = get_logger(__name__)

@pytest.fixture
def data_from_webhook():
    datas = []
    with open("api/wazzup/wazzap_hook_data.json","r", encoding="utf-8") as f:
        datas = json.loads(f.read())
    # logger.debug(f'result = {datas}')
    return datas

@pytest.mark.usefixtures("data_from_webhook")
class TestModels:
    def test_webhook(self, data_from_webhook, caplog):
        result = WazzupUtils.handle_message_from_hook(data_from_webhook)
        caplog.set_level(logging.DEBUG)
        logger.debug(f'result = {result}')
        # assert len(result) == 1 #TODO Доработать
        # assert result[0].phone == "79164516629"



