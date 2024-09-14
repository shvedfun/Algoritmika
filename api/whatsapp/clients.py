import http
import json
from abc import ABC, abstractmethod


from aiohttp import ClientSession, TCPConnector, ClientTimeout
from typing import Optional

from openai import base_url

from api.config import settings
from api.public.algv2.models import Message, Contact, PhoneMessage
from api.utils.logger import get_logger

from .wazzup_utils import WazzupUtils, WazzupClientStatic, WazzupClientData

logger = get_logger(__name__)


class WhatAppClient(ABC):
    @abstractmethod
    def send_message(self, phone_message: PhoneMessage, request_limit=10, request_timeout=10):
        pass

class WhatCrm(WhatAppClient):
    suffics = {'message': '/sendMessage'}

    @staticmethod
    def get_header_token(header_token: str) -> tuple:
        header, token = tuple(header_token.split())
        return header, token

    def get_common_headers(self):
        return {self.token_header: self.token, 'Content-type': 'application/json'}

    def __init__(self):
        self.base_url = settings.WHATCRM_BASE_URL
        self.token_header, self.token = self.get_header_token(settings.WHATCRM_TOKEN.split())

    async def send_message(self, phone_message: PhoneMessage, request_limit=10, request_timeout=10) -> [Optional[http.HTTPStatus], Optional[dict]]:
        session_config = {
            "base_url": self.base_url,
            "headers": self.get_common_headers(),
            "connector": TCPConnector(limit=request_limit),
            "timeout": ClientTimeout(total=request_timeout),
        }
        body = {'message': phone_message.text, 'phone': phone_message.phone}
        request_config = {
            "method": "POST",
            "url": f"/instances/{settings.WHATCRM_KEY}/sendMessage",
            "json": body
        }
        status, result = None, None
        async with ClientSession(**session_config) as session:
            async with session.request(**request_config) as response:
                result = await response.json()
                status = response.status
                logger.debug('status = %r, body = %r', status, result)
        return status, result


class WazzupClient(WazzupClientData, WazzupClientStatic, WazzupUtils, WhatAppClient):

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
        return status, result


def get_whatsapp_client() -> WhatAppClient:
    if settings.WHATAPP_CLIENT == "WAZZUP":
        return WazzupClient(url=settings.WAZZUP_URL, token=settings.WAZZUP_TOKEN)
    return WhatCrm()
