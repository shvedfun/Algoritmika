import http


from aiohttp import ClientSession, TCPConnector, ClientTimeout
from typing import Optional

from openai import base_url

from api.config import settings
from api.public.algv2.models import Message, Contact, PhoneMessage
from api.utils.logger import get_logger


logger = get_logger(__name__)


