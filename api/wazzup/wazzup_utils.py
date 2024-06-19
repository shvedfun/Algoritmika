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


class WazzupClient(WazzupClientData, WazzupClientStatic, WazzupUtils):

    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.channel_id = "e374b3cc-541c-40f2-a663-490043584700"
        self.chat_type = "whatsapp"

    def _prepare_url(self, suffics_key, id=None):
        url = self.url + self.suffics[suffics_key]
        if id is not None:
            url += '/' + str(id)
        return url

    def _get_headers(self) -> dict:
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }
        return headers

    async def _request_get(self, suffics_name, id=None, **kwargs):
        result = {}
        headers = self._get_headers()
        async with ClientSession(headers=headers) as session:
            url = self.url + self.suffics[suffics_name]
            if id:
                url += '/' + str(id)
            # logger.info(f'url = {url}')
            async with session.get(url=url, **kwargs) as response:
                # logger.info(f'resp.status = {response.status}, headers = {response.headers}')
                result = await response.read()
                status = response.status
            if status in (http.HTTPStatus.OK,
                          http.HTTPStatus.CREATED,
                          ):
                result = json.loads(result)
            else:
                result = {}
        return status, result

    async def _request_post(self, suffics_name, json_data, **kwargs):
        result = {}
        headers = self._get_headers()
        logger.debug(f'headers = {headers}')
        json_data = json.dumps(json_data)
        json_data = bytes(json_data, encoding='utf-8')
        logger.debug(f'json_data = {json_data}')
        async with ClientSession(headers=headers) as session:
            url = self.url + self.suffics[suffics_name]
            logger.info(f'url = {url}')
            async with session.post(url=url, headers=headers, data=json_data, **kwargs) as response:
                # logger.info(f'resp.status = {response.status}, headers = {response.headers}')
                result = await response.read()
                status = response.status
            if status in (http.HTTPStatus.OK,
                          http.HTTPStatus.CREATED,
                          ):
                result = json.loads(result)
        return status, result


    async def send_message(self, phone_message: PhoneMessage):
        logger.debug(f'phone_message = {phone_message}')
        payload = {
            "channelId": self.channel_id,
            "chatType": self.chat_type,
            "chatId": phone_message.phone,
            "text": phone_message.text
        }
        status, result = await self._request_post("message", json_data=payload)
        logger.debug(f'status = {status} result = {result}')
        return status


def get_wazzup_client():
    return WazzupClient(url=settings.WAZZUP_URL, token=settings.WAZZUP_TOKEN)

