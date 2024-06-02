import logging

from aiohttp import ClientSession

logger = logging.getLogger(__name__)


class AMOClient:
    base_url = ".amocrm.ru"
    suffics = {
        "leads": "/api/v4/leads",
        "pipelines": "/api/v4/leads/pipelines",
    }

    def __init__(self, url_prefix, long_token):
        self.url = "https://" + url_prefix + self.base_url
        self.token = long_token

    def _get_headers(self) -> dict:
        return {
            "Authorization": "Bearer " + self.token
        }

    async def _request_get(self, suffics_name, **kwargs):
        result = {}
        headers = self._get_headers()
        async with ClientSession(headers=headers) as session:
            url = self.url + self.suffics[suffics_name]
            async with session.get(url=url, **kwargs) as response:
                result = await response.json()
        return result

    async def get_leads(self, **kwargs):
        result = await self._request_get(suffics_name="leads", **kwargs)
        return result

    async def get_piplines(self, **kwargs):
        result = await self._request_get(suffics_name="pipelines", **kwargs)
        return result
