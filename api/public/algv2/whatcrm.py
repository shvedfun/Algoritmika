import datetime
import http.client
from uuid import UUID, uuid4
from typing import Union
from fastapi import APIRouter, Depends, Query, Request, Form, BackgroundTasks, HTTPException, Response
from sqlmodel import Session, select, desc
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from api.ydb_utils import db, db_executor
from api.utils.logger import get_logger
from api.public.algv2.models import WhatCrmMessage
from api.ydb_utils import db_executor

router = APIRouter()

logger = get_logger(__name__)

from ai_utils.client import get_ai_client

@router.post("/webhook")
async def handle_webhook(wcrm_data: WhatCrmMessage, response: Response):
    if not wcrm_data.message:
        response.status_code = http.HTTPStatus.OK
        return
    phone = wcrm_data.get_phone()
    text = wcrm_data.get_text()
    contact_id = db_executor.get_contact_id_by_phone(phone)
    if contact_id is None:
        logger.warning(f'Не нашел контакт с телефоном {phone}')
        return

    await get_ai_client().send_message2ai(contact_id, text)
    return

