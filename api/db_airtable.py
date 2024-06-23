from typing import Optional
from pyairtable import Api
from api.config import settings

class DBAirtable:

    def __init__(self, api_key: Optional[str]=None):
        self.api_key = api_key or settings.DB_AT_TOKEN

db_airtable = DBAirtable()