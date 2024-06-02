import http
import json
from api.utils.logger import logger_config
from aiohttp import ClientSession
import requests

logger = logger_config(__name__)


class AMOClientData:
    base_url = ".amocrm.ru"
    suffics = {
        "leads": "/api/v4/leads",
        "pipelines": "/api/v4/leads/pipelines",
        "contacts": "/api/v4/contacts",
    }
    pipelines = {'default': 8164598, 'AI': 8177166}
    pipelines_statuses = {
        8164598: {
            "Неразобранное": 66751006,
            "Первичный контакт": 66751010,
            "Переговоры": 66751014,
        },
        8177166: {
            "Неразобранное": 66838994,
            "Первичный контакт": 66838998,
            "Переговоры": 66839002,
            "Успешно реализовано": 142,
            "Закрыто и не реализовано": 143
        }
    }


class AMOClientStatic:
    @staticmethod
    def get_leads_from_response(response_dict: dict) -> list[dict]:
        leads = response_dict.get("_embedded", {}).get("leads", [])
        return leads

    @staticmethod
    def get_contact_ids_from_dict_lead(lead: dict) -> list[dict]:
        contacts = lead.get("_embedded", {}).get("contacts", [])
        return contacts

    @staticmethod
    def get_main_contact_id(contacts: list[dict]):
        result = None
        for contact in contacts:
            if contact.get('is_main'):
                return contact['id']
        return result

    @staticmethod
    def get_validated_contact(amo_contact: dict) -> dict:
        ai_contact = {}
        ai_contact['id'] = amo_contact['id']
        ai_contact['first_name'] = amo_contact['first_name']
        ai_contact['last_name'] = amo_contact['last_name']
        ai_contact['name'] = amo_contact['name']
        ai_contact['phone'] = None
        for cust_f in amo_contact["custom_fields_values"]:
            if cust_f.get("field_code") == "PHONE":
                ai_contact['phone'] = cust_f.get("values")[0]['value']
        return ai_contact



class AMOClient(AMOClientData, AMOClientStatic):

    def __init__(self, url_prefix, long_token):
        self.url = "https://" + url_prefix + self.base_url
        self.token = long_token

    def _get_headers(self) -> dict:
        headers = {
            "Authorization": "Bearer " + self.token,
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

    async def _request_patch(self, suffics_name, json, **kwargs):
        result = {}
        headers = self._get_headers()
        async with ClientSession(headers=headers) as session:
            url = self.url + self.suffics[suffics_name]
            # logger.info(f'url = {url}')
            async with session.patch(url=url, json=json, **kwargs) as response:
                # logger.info(f'resp.status = {response.status}, headers = {response.headers}')
                result = await response.read()
                status = response.status
            if status in (http.HTTPStatus.OK,
                          http.HTTPStatus.CREATED,
                          ):
                result = json.loads(result)
        return status, result

    async def get_leads(self, pipeline_id=None, **kwargs):
        pesult = []
        kwargs['params'] = kwargs.get('params', {})
        kwargs['params'] |= {'with': 'contacts'}
        if pipeline_id:
            kwargs['params'] |= {'filter[pipeline_id]': pipeline_id}
        logger.debug(f'kwargs = {kwargs}')
        status, result = await self._request_get(suffics_name="leads", **kwargs)
        logger.debug(f'status = {status}')
        return result

    async def patch_leads(self, json, **kwargs):
        status, result = await self._request_patch(suffics_name="leads", json=json, **kwargs)
        return result



    async def get_piplines(self, **kwargs):
        result = await self._request_get(suffics_name="pipelines", **kwargs)
        return result

    async def get_contact(self, contact_id, **kwargs):
        status, result = await self._request_get(suffics_name=f'contacts', id=contact_id)
        return result

