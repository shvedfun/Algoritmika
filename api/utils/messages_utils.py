import http
import json
import traceback
from datetime import datetime

from api.public.algv2.models import PhoneMessage, Message, Contact, Booking, BookingStatusEnum
from api.ydb_utils import db_executor
from amo_utils.client import AMOClient
from ai_utils.client import get_ai_client, AIClient
from api.utils.logger import get_logger
from api.whatsapp.clients import get_whatsapp_client
from api.config import settings

logger = get_logger(__name__)
logger.info("setting_id = %r", id(settings))

class MessagesUtils:

    @staticmethod
    async def handle_messages_from_client(phone_messages: list[PhoneMessage]):
        ai_client: AIClient = get_ai_client()
        for phone_message in phone_messages:
            contact_id: int = db_executor.get_contact_id_by_phone(phone=phone_message.chatid)
            if contact_id:
                db_contact = db_executor.get_contact(contact_id)
                params = json.loads(db_contact.params) if db_contact.params else {}
                if params.get("disable", False) == True:
                    logger.info("contact disabled = %s", str(contact_id))
                    return
                if phone_message.phone != phone_message.chatid and not (phone_message.message_id in settings.send_ai_ids):
                    db_executor.disable_contact(contact_id)
                    logger.info(
                        "disable contact_id = %r, phone = %r, author = %r, chatid = %r",
                        contact_id, phone_message.phone, phone_message.author, phone_message.chatid
                    )
                    return
                if phone_message.ack == 1:
                    message = Message(contact_id=contact_id, text=phone_message.text,
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
        for message in messages:
            contact = db_executor.get_contact(contact_id=message.contact_id)
            if contact:
                if (not contact.params) or (not (json.loads(contact.params).get("disable", False))):
                    phone = contact.phone
                    text = message.text
                    phone_message = PhoneMessage(phone=phone, text=text, created=message.created)
                    logger.info(f'send message 2 whatsapp_client phone_message = {phone_message}')
                    whatsapp_client = get_whatsapp_client(contact.partner)
                    status, payload = await whatsapp_client.send_message(phone_message)
                    if payload.get("id"):
                        settings.send_ai_ids.add(payload["id"])
                    if status not in (http.HTTPStatus.OK, http.HTTPStatus.CREATED):
                        logger.error(f'message not in whatsapp {message}')
                    db_executor.insert_message(message)
                else:
                    logger.info("Not send AI message to disabled contact = %r", contact)
            else:
                logger.info("Not send AI message to contact = %r", contact)
        return

    @staticmethod
    async def handle_booking(bk: Booking):
        result = {}
        # tst = datetime.datetime.utcnow().replace(microsecond=0, tzinfo=None)
        # if not bk.created:
        #     bk.created = tst
        # bk.updated = tst
        # group = db_executor.get_group(bk.group_id)
        # logger.debug(f'group = {group}')
        # result['group'] = group
        # n_book = db_executor.get_number_booking(bk.group_id)
        # logger.debug(f'n_book = {n_book}')
        # if n_book < group.get('capacity', -1):
        #     bk.status = BookingStatusEnum.ok
        # else:
        #     bk.status = BookingStatusEnum.rjct
        #     return bk
        # db_executor.upsert_booking(bk)

        return result


