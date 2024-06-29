import http
import traceback
import datetime

from fastapi import Response

from api.public.algv2.models import PhoneMessage, Message, Contact, Booking, BookingStatusEnum
from api.ydb_utils import ydb_executor
from api.ai_utils.client import get_ai_client, AIClient
from api.utils.logger import get_logger
from api.wazzup.wazzup_utils import get_wazzup_client
from api.amo_utils.client import AMOClient
from api.config import settings

logger = get_logger(__name__)

class MessagesUtils:

    @staticmethod
    async def handle_messages_from_client(phone_messages: list[PhoneMessage]):
        ai_client: AIClient = get_ai_client()
        for phone_message in phone_messages:
            contact: list[Contact] = ydb_executor.get_contact_id_by_phone(phone=phone_message.phone)
            if contact:
                message = Message(contact_id=contact, text=phone_message.text,
                                  created=phone_message.created,
                                  ai_id="",)
                try:
                    message: Message = ydb_executor.insert_message(message)
                    await ai_client.send_message2ai(message.contact_id, message=message.text)
                except Exception as e:
                    logger.error(f'Error = {e} {traceback.format_exc()}')
        return

    @staticmethod
    async def handle_message_from_ai(messages: list[Message]):
        wazzup_client = get_wazzup_client()
        for message in messages:
            contact = ydb_executor.get_contact(contact_id=message.contact_id)
            if contact:
                contact = contact[0]
                phone = contact.phone
                text = message.text
                phone_message = PhoneMessage(phone=phone, text=text, created=message.created)
                logger.debug(f'send message 2 wazzup {phone_message}')
                status = await wazzup_client.send_message(phone_message)

                if status not in (http.HTTPStatus.OK, http.HTTPStatus.CREATED):
                    logger.error(f'message not in wazzup {message}')
                ydb_executor.insert_message(message)
        return

    @staticmethod
    async def handle_booking(bk: Booking):
        amo_client = AMOClient(url_prefix=settings.AMO_URL, long_token=settings.AMO_TOKEN, )
        # exists_capacity = get_group_capacity_exists(group_id)
        tst = datetime.datetime.utcnow().replace(microsecond=0, tzinfo=None)
        if not bk.created:
            bk.created = tst
        bk.updated = tst
        group = ydb_executor.get_group(bk.group_id)
        logger.debug(f'group = {group}')
        if not group:
            bk.status = BookingStatusEnum.bad_data
            return bk
        n_book = ydb_executor.get_number_booking(bk.group_id)
        logger.debug(f'n_book = {n_book}')
        if n_book < group.get('capacity', -1):
            bk.status = BookingStatusEnum.ok
        else:
            bk.status = BookingStatusEnum.rjct
            return bk
        ydb_executor.upsert_booking(bk)
        lead_id = ydb_executor.get_lead_id_from_student_id(bk.student_id)
        if lead_id:
            await amo_client.lead_done(lead_id)
        return bk


