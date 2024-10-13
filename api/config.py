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
    # AMO_URL: str = 'turboaiagency'
    # AMO_TOKEN: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjRiYjkxMTVhYTNmYmI5OWYzNTcxYTM2M2ViMzdkNDJlOTEyNDk4YWZjOWJiZTdhMTQ2MWU1NjhmNjhiMjRiNzVhMzYyNDMwYjE2ZDg1M2VmIn0.eyJhdWQiOiI1OGI5NTliMi0wZjFiLTRkZTAtYmQ0ZS0wOTA0M2Y0NmNlMjIiLCJqdGkiOiI0YmI5MTE1YWEzZmJiOTlmMzU3MWEzNjNlYjM3ZDQyZTkxMjQ5OGFmYzliYmU3YTE0NjFlNTY4ZjY4YjI0Yjc1YTM2MjQzMGIxNmQ4NTNlZiIsImlhdCI6MTcxNzIyNzA4MywibmJmIjoxNzE3MjI3MDgzLCJleHAiOjE3NDg3MzYwMDAsInN1YiI6IjExMDQ0NTc4IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxNzQ4NzU0LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiOWZkZGU3N2UtNjEzOS00OTIxLWI4ODMtODcxODBiOWFiZDQzIn0.KAbmdEhQ6u-5znl3YagjiUv3_6NEo8-G1dg6D_vVOs9BV1OG9g3E3I9wdrFVyvZQtvwe0PLsYdG5yFGhcYLuUr5yB9UHTE6ozBmw4OSeiko0JhHVi4MWHiL5irZrzjxc1kcyFU0LEoKe264iWPZxRoYwVCdLiK0Dw2l7hLiake9pLZ4JuaOF5BG4qrMwvSHc82bYifAAhCNsmhXFFGE7AjjxUxLNnrN6G0kv-1gsF6TKXOmIM-UAEI8M1dqpqJdAm8lEiVY8LfAb45sWEBa96eCoL3SvluhoV1usQbDeJnv9hvr0anzJTAAeVK3Cf3I8KjzWKCrugGLeidM5zysnRg" #os.getenv("AMO_TOKEN", "")
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
            "Не отвечает": "8689278",
            "Отказ": "8689282"
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
            },
            "8689278": {
                "Первичный контакт": 70404106,
                "Успешно реализовано": 142
            },
            "8689282": {
                "Первичный контакт": 70404122,
                "Успешно реализовано": 142
            }
        },
    },
    "dandykit": {
        "WHATCRM_KEY": "f892234183f4da06aa73df8698fa0efb",
        "WHATCRM_TOKEN": "X-Crm-Token 6a9fb48a08cd959820e783bfdda2e3df",
        "AMO_URL": "dandykit",
        "AMO_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImFmMDQzMjEyYjQ0NDAwZjFmZTQzZmRkYjY2YWZiNzliZjA2NjRhYTQyNzhlZDFjMTkzZTAzYTNiMzk5YTE5YWFlZWI5NjZmN2IyYzJlOTlmIn0.eyJhdWQiOiIxOTMwYzNhZS05ODBjLTRhNjItOTZiYS02MTA4NWFlMTJhNGIiLCJqdGkiOiJhZjA0MzIxMmI0NDQwMGYxZmU0M2ZkZGI2NmFmYjc5YmYwNjY0YWE0Mjc4ZWQxYzE5M2UwM2EzYjM5OWExOWFhZWViOTY2ZjdiMmMyZTk5ZiIsImlhdCI6MTcyNzU4NDgxOSwibmJmIjoxNzI3NTg0ODE5LCJleHAiOjE4ODUyNDgwMDAsInN1YiI6IjExNTc4NDY2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxOTc3MTE0LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiY2RlN2JlZmYtZDg1My00OGY3LTlhNjYtNDY5Njc1M2Y5NjQ3IiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.fpXEdAy10ymK2rlfGI8AO2yGFM7I4y2co3HcKKLAmBh0LUioYAVK05CMpjoqVE5dMthnYf89_CyZzIJODuWB6MUpizVzkkq5G8nbTMd0TNYGWvACQ4E4fLrzZ5jOMDR6XE7gCF6DS15E-nT-y2Mi_oWUnGhnfGq6aFFpNNMF7DpD3hVEiIrGf1i5iyO0KMf6n_5Yk7j86F27i8RiEBizHjzFzxbz4a3fXsOF5LuxgL6wWePCFQ5AHherS9zqDSDDdSdSvWDnc1MZoSlznIPxEQLDmo8Mk1hHqCiouvIl0LqKS04-SUhXkmuItOGnRmqELNfQeRuqXcwGhDQDCGLKRA",
        "pipelines": {
            "default": "8686626",
            "AI": "8689246",
            "Human": "8689254",
            "Записаны": "8689258",
            "Не отвечает": "8689266",
            "Отказ": "8689270"
        },
        "pipelines_statuses": {
            "8686626": {
                "Неразобранное": 70386602,
                "Первичный контакт": 70386606,
                "Переговоры": 70386610
            },
            "8689246": {
                "Неразобранное": 66838994,
                "Первичный контакт": 70403954,
                "Переговоры": 70403958,
                "Успешно реализовано": 142,
                "Закрыто и не реализовано": 143
            },
            "8689254": {
                "Неразобранное": 70403950,
                "Первичный контакт": 70403990,
                "Переговоры": 70403994,
                "Принимают решение": 70403998
            },
            "8689258": {
                "Первичный контакт": 70404006,
                "Успешно реализовано": 142
            },
            "8689266": {
                "Первичный контакт": 70404054,
                "Успешно реализовано": 142
            },
            "8689270": {
                "Первичный контакт": 70404070,
                "Успешно реализовано": 142
            },
        },
    },

}
settings.partners = partners

class TestSettings(Settings):
    class Config:
        case_sensitive = True


test_settings = TestSettings()
