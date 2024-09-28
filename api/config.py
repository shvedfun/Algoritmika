import os
import secrets
from typing import Literal

from pydantic_settings import BaseSettings


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
    AMO_URL: str = 'turboaiagency'
    AMO_TOKEN: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjRiYjkxMTVhYTNmYmI5OWYzNTcxYTM2M2ViMzdkNDJlOTEyNDk4YWZjOWJiZTdhMTQ2MWU1NjhmNjhiMjRiNzVhMzYyNDMwYjE2ZDg1M2VmIn0.eyJhdWQiOiI1OGI5NTliMi0wZjFiLTRkZTAtYmQ0ZS0wOTA0M2Y0NmNlMjIiLCJqdGkiOiI0YmI5MTE1YWEzZmJiOTlmMzU3MWEzNjNlYjM3ZDQyZTkxMjQ5OGFmYzliYmU3YTE0NjFlNTY4ZjY4YjI0Yjc1YTM2MjQzMGIxNmQ4NTNlZiIsImlhdCI6MTcxNzIyNzA4MywibmJmIjoxNzE3MjI3MDgzLCJleHAiOjE3NDg3MzYwMDAsInN1YiI6IjExMDQ0NTc4IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxNzQ4NzU0LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiOWZkZGU3N2UtNjEzOS00OTIxLWI4ODMtODcxODBiOWFiZDQzIn0.KAbmdEhQ6u-5znl3YagjiUv3_6NEo8-G1dg6D_vVOs9BV1OG9g3E3I9wdrFVyvZQtvwe0PLsYdG5yFGhcYLuUr5yB9UHTE6ozBmw4OSeiko0JhHVi4MWHiL5irZrzjxc1kcyFU0LEoKe264iWPZxRoYwVCdLiK0Dw2l7hLiake9pLZ4JuaOF5BG4qrMwvSHc82bYifAAhCNsmhXFFGE7AjjxUxLNnrN6G0kv-1gsF6TKXOmIM-UAEI8M1dqpqJdAm8lEiVY8LfAb45sWEBa96eCoL3SvluhoV1usQbDeJnv9hvr0anzJTAAeVK3Cf3I8KjzWKCrugGLeidM5zysnRg" #os.getenv("AMO_TOKEN", "")
    WAZZUP_URL: str = "https://api.wazzup24.com"
    WAZZUP_TOKEN: str = "Bearer 32fd6c110b65434fa87b47f25f07cb2d" #os.getenv("WAZZUP_TOKEN", "")
    IS_LOCAL: int = int(os.getenv("IS_LOCAL", 0))
    partners: dict = {}

    class ConfigDict:
        case_sensitive = True


settings = Settings()


partners = {
    "turboagency": {
        "WHATCRM_KEY": "d6714798e3ee84633693c5b71705b2ea",
        "WHATCRM_TOKEN": "X-Crm-Token 6a9fb48a08cd959820e783bfdda2e3df",
        "AMO_URL": "turboaiagency",
        "AMO_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjRiYjkxMTVhYTNmYmI5OWYzNTcxYTM2M2ViMzdkNDJlOTEyNDk4YWZjOWJiZTdhMTQ2MWU1NjhmNjhiMjRiNzVhMzYyNDMwYjE2ZDg1M2VmIn0.eyJhdWQiOiI1OGI5NTliMi0wZjFiLTRkZTAtYmQ0ZS0wOTA0M2Y0NmNlMjIiLCJqdGkiOiI0YmI5MTE1YWEzZmJiOTlmMzU3MWEzNjNlYjM3ZDQyZTkxMjQ5OGFmYzliYmU3YTE0NjFlNTY4ZjY4YjI0Yjc1YTM2MjQzMGIxNmQ4NTNlZiIsImlhdCI6MTcxNzIyNzA4MywibmJmIjoxNzE3MjI3MDgzLCJleHAiOjE3NDg3MzYwMDAsInN1YiI6IjExMDQ0NTc4IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxNzQ4NzU0LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiOWZkZGU3N2UtNjEzOS00OTIxLWI4ODMtODcxODBiOWFiZDQzIn0.KAbmdEhQ6u-5znl3YagjiUv3_6NEo8-G1dg6D_vVOs9BV1OG9g3E3I9wdrFVyvZQtvwe0PLsYdG5yFGhcYLuUr5yB9UHTE6ozBmw4OSeiko0JhHVi4MWHiL5irZrzjxc1kcyFU0LEoKe264iWPZxRoYwVCdLiK0Dw2l7hLiake9pLZ4JuaOF5BG4qrMwvSHc82bYifAAhCNsmhXFFGE7AjjxUxLNnrN6G0kv-1gsF6TKXOmIM-UAEI8M1dqpqJdAm8lEiVY8LfAb45sWEBa96eCoL3SvluhoV1usQbDeJnv9hvr0anzJTAAeVK3Cf3I8KjzWKCrugGLeidM5zysnRg",
        "pipelines": {
            "default": "8164598",
            "AI": "8177166",
            "Human": "8232310",
            "Записаны": "8294854",
            "Не отвечает": "8232310",
            "Отказ": "8232310"
        },
        "pipelines_statuses": {
            "8164598": {
                "Неразобранное": 66751006,
                "Первичный контакт": 66751010,
                "Переговоры": 66751014
            },
            "8177166": {
                "Неразобранное": 66838994,
                "Первичный контакт": 66838998,
                "Переговоры": 66839002,
                "Успешно реализовано": 142,
                "Закрыто и не реализовано": 143
            },
            "8232310": {
                "Неразобранное": 67221122,
                "Первичный контакт": 67221126,
                "Переговоры": 67221130,
                "Принимают решение": 67221134
            },
            "8294854": {
                "Первичный контакт": 67655354,
                "Успешно реализовано": 142
            }
        },
    },
    "dandykit": {
        "WHATCRM_KEY": "d6714798e3ee84633693c5b71705b2ea",
        "WHATCRM_TOKEN": "X-Crm-Token 6a9fb48a08cd959820e783bfdda2e3df",
        "AMO_URL": "dandykit",
        "AMO_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImMzMTkzZDAyY2E0ODQ4YTc2ZTY0YjQ0NDNmZjlhZDc0YWMxYWVlMTI4NTE5NTUyNTQ0YzExM2ZiMjg2YjhiOTc5MDBiMTkzYmQxZTU0Zjk5In0.eyJhdWQiOiIxOTMwYzNhZS05ODBjLTRhNjItOTZiYS02MTA4NWFlMTJhNGIiLCJqdGkiOiJjMzE5M2QwMmNhNDg0OGE3NmU2NGI0NDQzZmY5YWQ3NGFjMWFlZTEyODUxOTU1MjU0NGMxMTNmYjI4NmI4Yjk3OTAwYjE5M2JkMWU1NGY5OSIsImlhdCI6MTcyNzU0MjY2NywibmJmIjoxNzI3NTQyNjY3LCJleHAiOjE4ODUyNDgwMDAsInN1YiI6IjExNTc4NDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxOTc3MTE0LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiOWY4MmE2MTEtMjc0Zi00YzI5LWFiNDAtNGNjNDU3YzE2NjAxIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.pPPiO1aGOqGiv76PtnVsk_mhfyblmpTj5wXlX16qsey73hNtq6PYg1gqfBg0Su87aim0DuiHmodMt-zAe3dHcn4It731vSeko7-Jf2YEJ6k7_Nhs7-DWTjqaKZeVp_MuCLM0Hj6H99bQxWRQCFik957-KbbotO3bOi0405i-8AC3fL2izJsyzCPDPpTfPC6OFCQsjSmvSlavV4t6CpiZ9eS5ZY6mHb52dWBJisbmTOGox5qd8o8n-6H8xMyVsozGbd-ASbCueAHB7COEWKHbV5pmbMv8LtUPUcLp7THwU-4gMoEkKtskK-k44z3wXfX-72589SHaDf8kzJwTEvvq7w",
        "pipelines": {
            "default": "8164598",
            "AI": "8177166",
            "Human": "8232310",
            "Записаны": "8294854",
            "Не отвечает": "8232310",
            "Отказ": "8232310"
        },
        "pipelines_statuses": {
            "8164598": {
                "Неразобранное": 66751006,
                "Первичный контакт": 66751010,
                "Переговоры": 66751014
            },
            "8177166": {
                "Неразобранное": 66838994,
                "Первичный контакт": 66838998,
                "Переговоры": 66839002,
                "Успешно реализовано": 142,
                "Закрыто и не реализовано": 143
            },
            "8232310": {
                "Неразобранное": 67221122,
                "Первичный контакт": 67221126,
                "Переговоры": 67221130,
                "Принимают решение": 67221134
            },
            "8294854": {
                "Первичный контакт": 67655354,
                "Успешно реализовано": 142
            }
        },
    },

}
settings.partners = partners

class TestSettings(Settings):
    class Config:
        case_sensitive = True


test_settings = TestSettings()
