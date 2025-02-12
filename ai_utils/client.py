import http
import json
from api.utils.logger import get_logger
from aiohttp import ClientSession
from api.public.algv2.models import Contact
from api.config import settings

logger = get_logger(__name__)

logger.info("setting_id = %r", id(settings))

TEST = False

class AIClientData:
    suffics = {
        "leads": "/api/leads",
        "pipelines": "/api/leads/pipelines",
        "contacts": "/api/contact",
        "message": "/api/message",
    }


class AIClientStatic:
    @staticmethod
    def get_validated_contact(amo_contact: dict) -> dict:
        ai_contact = {}
        ai_contact['id'] = amo_contact['id']
        ai_contact['name'] = amo_contact['first_name']
        ai_contact['surname'] = amo_contact['last_name']
        # for cust_f in amo_contact["custom_fields_values"]:
        #     if cust_f.get("field_code") == "PHONE":
        #         ai_contact['phone'] = cust_f.get("values")[0]['value']
        return ai_contact


class AIClient(AIClientData, AIClientStatic):

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def _prepare_url(self, suffics_key, id=None):
        url = self.url + self.suffics[suffics_key]
        if id is not None:
            url += '/' + str(id)
        return url

    def _get_headers(self) -> dict:
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }
        return headers

    async def _request_get(self, url, **kwargs):
        result = {}
        headers = self._get_headers()
        async with ClientSession(headers=headers) as session:
            async with session.get(url=url, **kwargs) as response:
                result = await response.read()
                status = response.status
            if status in (http.HTTPStatus.OK,
                          http.HTTPStatus.CREATED,
                          ):
                result = json.loads(result)
            else:
                result = {}
        return status, result

    async def _request_post(self, url: str, data: dict, **kwargs):
        if TEST:
            return http.HTTPStatus.OK, {}
        result = {}
        headers = self._get_headers()
        async with ClientSession(headers=headers) as session:
            async with session.post(url=url, json=data, headers=headers, **kwargs) as response:
                result = await response.read()
                status = response.status
            if status in (http.HTTPStatus.OK,
                          http.HTTPStatus.CREATED,
                          ):
                result = json.loads(result)
            else:
                result = {}
        return status, result

    async def send_newcontact2ai(self, contact: Contact) -> dict:
        url = self._prepare_url('contacts')
        logger.debug(f'contact = {contact}')
        payload = {
            "user_id": contact.get("id"),
            "name": contact.get("name"),
            "surname": contact.get("last_name"),
            "params": contact.get("params"),
            "partner": contact.get("partner"),
        }
        status, result = await self._request_post(url, payload)
        return result

    async def send_message2ai(self, contact_id: int, message: str) -> dict:
        url = self._prepare_url('message')
        logger.debug(f'url = {url}')
        payload = {"message": message, "user_id": contact_id}
        logger.debug(f'payload {payload}')
        status, result = await self._request_post(url, payload)
        logger.debug(f'status = {status}, result = {result}')
        return result


def get_ai_client():
    return AIClient(settings.AI_URL, settings.AI_TOKEN)