import http
import traceback
from datetime import datetime

from api.public.algv2.models import PhoneMessage, Message, Contact
from api.ydb_utils import db_executor
from ai_utils.client import get_ai_client, AIClient
from api.utils.logger import get_logger
from api.wazzup.wazzup_utils import WazzupClient, get_wazzup_client

logger = get_logger(__name__)

class MessagesUtils:

    @staticmethod
    async def handle_messages_from_client(phone_messages: list[PhoneMessage]):
        ai_client: AIClient = get_ai_client()
        for phone_message in phone_messages:
            contact: list[Contact] = db_executor.get_contact_id_by_phone(phone=phone_message.phone)
            if contact:
                contact = contact[0]
                message = Message(contact_id=contact.id, text=phone_message.text,
                                  created=phone_message.created,
                                  ai_id="",)
                try:
                    message: Message = db_executor.insert_message(message)
                    await ai_client.send_message2ai(message.contact_id, message=message.text)
                except Exception as e:
                    logger.error(f'Error = {e} {traceback.format_exc()}')
        return

    @staticmethod
    async def handle_message_from_ai(messages: list[Message]):
        wazzup_client = get_wazzup_client()
        for message in messages:
            contact = db_executor.get_contact(contact_id=message.contact_id)
            if contact:
                contact = contact[0]
                phone = contact.phone
                text = message.text
                phone_message = PhoneMessage(phone=phone, text=text, created=message.created)
                status = await wazzup_client.send_message(phone_message)

                if status not in (http.HTTPStatus.OK, http.HTTPStatus.CREATED):
                    logger.error(f'message not in wazzup {message}')
                db_executor.insert_message(message)
        return




