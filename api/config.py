import json
import os
import secrets
import logging
from typing import Literal

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    PROJECT_NAME: str = f"Algoritmika"
    DESCRIPTION: str = "For Algoritmika"
    ENV: Literal["development", "staging", "production"] = "development"
    VERSION: str = "0.3"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/algoritmika"
    API_USERNAME: str = os.getenv('USERNAME', '') #"svc_test"
    API_PASSWORD: str = os.getenv('PASSWORD', '') #"superstrongpassword"
    WHATCRM_BASE_URL: str = "https://api.whatcrm.net/"
    # WHATCRM_KEY: str="d6714798e3ee84633693c5b71705b2ea"
    # WHATCRM_TOKEN: str = "X-Crm-Token 6a9fb48a08cd959820e783bfdda2e3df"
    WHATSAPP_CLIENT: str = "WHATCRM"
    AI_URL: str = "http://algoritmica-assistant.turboai.agency"
    AI_TOKEN: str = ""
    # AMO_URL: str = 'turboaiagency'
    # AMO_TOKEN: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjRiYjkxMTVhYTNmYmI5OWYzNTcxYTM2M2ViMzdkNDJlOTEyNDk4YWZjOWJiZTdhMTQ2MWU1NjhmNjhiMjRiNzVhMzYyNDMwYjE2ZDg1M2VmIn0.eyJhdWQiOiI1OGI5NTliMi0wZjFiLTRkZTAtYmQ0ZS0wOTA0M2Y0NmNlMjIiLCJqdGkiOiI0YmI5MTE1YWEzZmJiOTlmMzU3MWEzNjNlYjM3ZDQyZTkxMjQ5OGFmYzliYmU3YTE0NjFlNTY4ZjY4YjI0Yjc1YTM2MjQzMGIxNmQ4NTNlZiIsImlhdCI6MTcxNzIyNzA4MywibmJmIjoxNzE3MjI3MDgzLCJleHAiOjE3NDg3MzYwMDAsInN1YiI6IjExMDQ0NTc4IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxNzQ4NzU0LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiOWZkZGU3N2UtNjEzOS00OTIxLWI4ODMtODcxODBiOWFiZDQzIn0.KAbmdEhQ6u-5znl3YagjiUv3_6NEo8-G1dg6D_vVOs9BV1OG9g3E3I9wdrFVyvZQtvwe0PLsYdG5yFGhcYLuUr5yB9UHTE6ozBmw4OSeiko0JhHVi4MWHiL5irZrzjxc1kcyFU0LEoKe264iWPZxRoYwVCdLiK0Dw2l7hLiake9pLZ4JuaOF5BG4qrMwvSHc82bYifAAhCNsmhXFFGE7AjjxUxLNnrN6G0kv-1gsF6TKXOmIM-UAEI8M1dqpqJdAm8lEiVY8LfAb45sWEBa96eCoL3SvluhoV1usQbDeJnv9hvr0anzJTAAeVK3Cf3I8KjzWKCrugGLeidM5zysnRg" #os.getenv("AMO_TOKEN", "")
    WAZZUP_URL: str = "https://api.wazzup24.com"
    WAZZUP_TOKEN: str = "Bearer 32fd6c110b65434fa87b47f25f07cb2d" #os.getenv("WAZZUP_TOKEN", "")
    IS_LOCAL: int = int(os.getenv("IS_LOCAL", 0))
    LOG_LEVEL: int = int(os.getenv("LOG_LEVEL", "20"))
    partners: dict = {}
    send_ai_ids: set | None  = None

    class ConfigDict:
        case_sensitive = True


settings = Settings()

with open("ext_conf/secrets_conf.json", "r", encoding="utf-8") as f:
    partners = json.loads(f.read())

settings.partners = partners
settings.send_ai_ids = set()
logger.info("setting_id = %r", id(settings))

class TestSettings(Settings):
    class Config:
        case_sensitive = True


test_settings = TestSettings()
