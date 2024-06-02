import asyncio
import json

from amo_utils.client import AMOClient
from api.utils.logger import logger_config
from api.db_utils import db_connector

logger = logger_config(__name__)

class BackgroundManager:

    def __init__(
            self, amo_client : AMOClient = None,
            sleep_time:int = 1,
            sleep_contact2ai_message: int = 15,
            sleep_ai2contact_message: int = 20,
            sleep_new_contact: int = 5
    ) -> None:
        self.sleep_time = sleep_time
        self.sleep_new_contact = sleep_new_contact
        self.sleep_contact2ai_message = sleep_contact2ai_message
        self.sleep_ai2contact_message = sleep_ai2contact_message
        self.amo_client = AMOClient(
            url_prefix='turboaiagency',
            long_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjRiYjkxMTVhYTNmYmI5OWYzNTcxYTM2M2ViMzdkNDJlOTEyNDk4YWZjOWJiZTdhMTQ2MWU1NjhmNjhiMjRiNzVhMzYyNDMwYjE2ZDg1M2VmIn0.eyJhdWQiOiI1OGI5NTliMi0wZjFiLTRkZTAtYmQ0ZS0wOTA0M2Y0NmNlMjIiLCJqdGkiOiI0YmI5MTE1YWEzZmJiOTlmMzU3MWEzNjNlYjM3ZDQyZTkxMjQ5OGFmYzliYmU3YTE0NjFlNTY4ZjY4YjI0Yjc1YTM2MjQzMGIxNmQ4NTNlZiIsImlhdCI6MTcxNzIyNzA4MywibmJmIjoxNzE3MjI3MDgzLCJleHAiOjE3NDg3MzYwMDAsInN1YiI6IjExMDQ0NTc4IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxNzQ4NzU0LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiOWZkZGU3N2UtNjEzOS00OTIxLWI4ODMtODcxODBiOWFiZDQzIn0.KAbmdEhQ6u-5znl3YagjiUv3_6NEo8-G1dg6D_vVOs9BV1OG9g3E3I9wdrFVyvZQtvwe0PLsYdG5yFGhcYLuUr5yB9UHTE6ozBmw4OSeiko0JhHVi4MWHiL5irZrzjxc1kcyFU0LEoKe264iWPZxRoYwVCdLiK0Dw2l7hLiake9pLZ4JuaOF5BG4qrMwvSHc82bYifAAhCNsmhXFFGE7AjjxUxLNnrN6G0kv-1gsF6TKXOmIM-UAEI8M1dqpqJdAm8lEiVY8LfAb45sWEBa96eCoL3SvluhoV1usQbDeJnv9hvr0anzJTAAeVK3Cf3I8KjzWKCrugGLeidM5zysnRg"
        )

    async def run(self):
        count = 1
        while True:
            if count % self.sleep_contact2ai_message == 0:
                await self.do_contact2ai_message()
            if count % self.sleep_ai2contact_message == 0:
                await self.do_ai2contact_message()
            if count % self.sleep_new_contact == 0:
                await self.do_new_lead()
            await asyncio.sleep(self.sleep_time)
            count += 1

    async def do_new_lead(self):
        pipelile_id = AMOClient.pipelines.get('default')
        result = await self.amo_client.get_leads(pipeline_id=pipelile_id)
        logger.debug(f'result = {result}')
        leads = self.amo_client.get_leads_from_response(result)
        for lead in leads:
            if lead.get('status_id', 0) == self.amo_client.pipelines_statuses[pipelile_id]["Первичный контакт"]:
                contacts = AMOClient.get_contact_ids_from_dict_lead(lead)
                main_contact_id = self.amo_client.get_main_contact_id(contacts)
                logger.debug(f'main_contact_id = {main_contact_id}')
                if main_contact_id:
                    contact = await self.amo_client.get_contact(main_contact_id)
                    validated_contact = self.amo_client.get_validated_contact(contact)
                    logger.info(f'validated_contact = {validated_contact}')
                    db_connector.upsert_contact_from_amo(validated_contact)
                    new_pipeline_id = self.amo_client.pipelines['AI']
                    new_status_id = self.amo_client.pipelines_statuses[new_pipeline_id]["Первичный контакт"]
                    data_patch_leads = [{'id': lead['id'],
                                         'pipeline_id': new_pipeline_id,
                                         'status_id': new_status_id,
                                         },
                                        ]
                    data_patch_leads = json.dumps(data_patch_leads)
                    logger.debug(f'data_patch_leads = {data_patch_leads}')
                    result = await self.amo_client.patch_leads(json=data_patch_leads)
                    logger.debug(f'result = {result}')
                else:
                    pass
                    # move_lead_

        logger.info(f'do_new_contact result = {result}')
        return result

    async def do_contact2ai_message(self):
        logger.info(f'do_contact2ai_message')
        result = []
        return result

    async def do_ai2contact_message(self):
        logger.info(f'do_ai2contact_message')
        result = []
        return result