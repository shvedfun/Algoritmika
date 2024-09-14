import http
import json
import datetime
import traceback

from aiohttp import ClientSession
from api.config import settings

from api.public.algv2.models import PhoneMessage
from api.utils.logger import get_logger

logger = get_logger(__name__)



class WazzupUtils:
    @staticmethod
    def handle_message_from_hook(body_hook: dict) -> list[PhoneMessage]:
        results = []
        for message in body_hook.get('messages', []):
            if message.get('status') == 'inbound':
                tst = None
                text = message.get('text') if message.get('text') else message.get("_data", {}).get("body", "")
                phone = message.get("chatId").replace("@c.us", "")
                try:
                    dt = message.get('dateTime')
                    if isinstance(dt, str):
                        dt = dt[:19]
                        logger.debug(f'dt = {dt}')
                        try:
                            tst = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
                        except Exception as e:
                            logger.error(f'Error {e} {traceback.format_exc()}')
                            tst = None
                    if not tst:
                        tst = datetime.datetime.fromtimestamp(message.get("timestamp")) if message.get("timestamp") else None
                except Exception as e:
                    logger.error(f'Error {e} {traceback.format_exc()}')
                    tst = None
                if phone and text and tst:
                    new_message = PhoneMessage(text=text, phone=phone, created=tst)
                    results.append(new_message)
        return results


class WazzupClientData:
    suffics = {
        "message": "/v3/message",
    }


class WazzupClientStatic:
    pass


