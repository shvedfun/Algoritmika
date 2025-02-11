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
    logger.info(f'whatcrm webhook body = {body}')
    for message in body.get('messages', []):
        if (message.get("ack") is not None) and (message["ack"] in [0, 1]) and message["type"] == "chat":
            text = message['body']
            phone = message['from'].replace("@c.us", "")
            author = message.get('author', "").replace("@c.us", "")
            chatid = message.get('chatId', "").replace("@c.us", "")
            tst = datetime.fromtimestamp(message["timestamp"], timezone.utc)
            ack = message.get("ack")
            message_id = message.get("id", "")
            new_message = PhoneMessage(text=text, phone=phone, created=tst, author=author, chatid=chatid, ack=ack, message_id=message_id)
            logger.debug(f'phone_messages = {new_message}')
            background_tasks.add_task(MessagesUtils.handle_messages_from_client, [new_message])
            response.status_code = http.HTTPStatus.CREATED
    return

