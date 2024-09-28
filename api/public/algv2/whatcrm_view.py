import http
from datetime import datetime, timezone
from fastapi import APIRouter, Response, BackgroundTasks
from api.utils.logger import get_logger
from api.utils.messages_utils import MessagesUtils

from api.public.algv2.models import PhoneMessage
router = APIRouter()

logger = get_logger(__name__)

from ai_utils.client import get_ai_client

@router.post("/webhook")
async def handle_webhook(body: dict, response: Response, background_tasks: BackgroundTasks):
    logger.debug(f'whatcrm webhook body = {body}')
    for message in body.get('messages', []):
        if message["ack"] == 1 and message["type"] == "chat":
            text = message['body']
            phone = message['from'].replace("@c.us", "")
            tst = datetime.fromtimestamp(message["timestamp"], timezone.utc)
            new_message = PhoneMessage(text=text, phone=phone, created=tst)
            logger.debug(f'phone_messages = {new_message}')
            background_tasks.add_task(MessagesUtils.handle_messages_from_client, [new_message])
            response.status_code = http.HTTPStatus.CREATED
    return

