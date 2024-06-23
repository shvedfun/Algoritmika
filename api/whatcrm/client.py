import http
from aiohttp import ClientSession
# from aiohttp.client import S
from typing import Optional

from api.config import settings
from api.public.algv2.models import Message, Contact
from api.utils.logger import get_logger


logger = get_logger(__name__)


class WhatCrm:
    suffics = {'message': '/api/message'}

    @staticmethod
    def get_header_token(header_token: str) -> tuple:
        header, token = tuple(header_token.split())
        return header, token

    def get_common_headers(self):
        return {self.token_header: self.token, 'Content-type': 'application/json'}

    def __init__(self):
        self.url = settings.WHATCRM_URL
        self.token_header, self.token = self.get_header_token(settings.WHATCRM_TOKEN.split())

    async def send_message(self, message: Message, contact: Contact) -> [Optional[http.HTTPStatus], Optional[dict]]:
        body = {'message': message.text, 'phone': contact.phone}
        url = self.url + self.suffics['message']
        status, result = None, None
        async with ClientSession(headers=self.get_common_headers()) as session:
            async with session.post(url=url, data=body) as response:
                result = await response.json()
                logger.debug(f'body = {result}')
                status = response.status
        return status
