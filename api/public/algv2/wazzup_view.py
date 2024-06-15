import http.client
from fastapi import APIRouter, Response
from api.utils.logger import get_logger


router = APIRouter()

logger = get_logger(__name__)

from ai_utils.client import get_ai_client

@router.post("/webhook")
async def handle_webhook(wazzup_data: dict, response: Response):
    logger.debug(f'body = {wazzup_data}')
    # if not wcrm_data.message:
    #     response.status_code = http.HTTPStatus.OK
    #     return
    # phone = wcrm_data.get_phone()
    # text = wcrm_data.get_text()
    # contact_id = db_executor.get_contact_id_by_phone(phone)
    # if contact_id is None:
    #     logger.warning(f'Не нашел контакт с телефоном {phone}')
    #     return
    #
    # await get_ai_client().send_message2ai(contact_id, text)
    response.body = wazzup_data
    response.status_code = http.HTTPStatus.OK
    return

