import http


from aiohttp import ClientSession, TCPConnector, ClientTimeout
from typing import Optional

from openai import base_url

from api.config import settings
from api.public.algv2.models import Message, Contact, PhoneMessage
from api.utils.logger import get_logger


logger = get_logger(__name__)


class WhatCrm:
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
