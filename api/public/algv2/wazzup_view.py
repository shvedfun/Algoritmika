import http.client
from fastapi import APIRouter, Response, BackgroundTasks
from api.utils.logger import get_logger
from api.whatsapp.wazzup_utils import WazzupUtils
from api.public.algv2.models import PhoneMessage
from api.utils.messages_utils import MessagesUtils


router = APIRouter()

logger = get_logger(__name__)



@router.post("/webhook")
async def handle_webhook(wazzup_data: dict, response: Response, background_tasks: BackgroundTasks):
    logger.debug("Exit")
    return
    logger.debug(f'body = {wazzup_data}')
    phone_messages: list[PhoneMessage] = WazzupUtils.handle_message_from_hook(wazzup_data)
    if phone_messages:
        logger.debug(f'phone_messages = {phone_messages}')
        background_tasks.add_task(MessagesUtils.handle_messages_from_client, phone_messages)
    response.body = wazzup_data
    response.status_code = http.HTTPStatus.OK
    return

