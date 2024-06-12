import asyncio
import json

from amo_utils.client import AMOClient
from ai_utils.client import AIClient
from api.utils.logger import get_logger
from api.ydb_utils import db_executor
from api.config import settings

logger = get_logger(__name__)


class BackgroundManager:

    def __init__(
            self, amo_client : AMOClient = None,
            ai_client: AIClient = None,
            sleep_time:int = 1,
            sleep_contact2ai_message: int = 15,
            sleep_ai2contact_message: int = 20,
            sleep_new_contact: int = 5
    ) -> None:
        self.sleep_time = sleep_time
        self.sleep_new_contact = sleep_new_contact
        self.sleep_contact2ai_message = sleep_contact2ai_message
        self.sleep_ai2contact_message = sleep_ai2contact_message
        self.amo_client = amo_client or AMOClient(
            url_prefix= settings.AMO_URL,
            long_token= settings.AMO_TOKEN,
        )
        self.aiclient = ai_client or AIClient(url='', token='')

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
                    if validated_contact['phone']:
                        db_executor.upsert_contact_from_amo(validated_contact)
                        new_pipeline_id = self.amo_client.pipelines['AI']
                        new_status_id = self.amo_client.pipelines_statuses[new_pipeline_id]["Первичный контакт"]
                        data_patch_leads = [{'id': lead['id'],
                                             'pipeline_id': new_pipeline_id,
                                             'status_id': new_status_id,
                                             },
                                            ]
                        logger.debug(f'data_patch_leads = {data_patch_leads}')
                        result = await self.amo_client.patch_leads(json_data=data_patch_leads)
                        logger.debug(f'result = {result}')
                        ai_result = await self.aiclient.send_newcontact2ai(validated_contact)

                    else:
                        new_pipeline_id = self.amo_client.pipelines['Human']
                        new_status_id = self.amo_client.pipelines_statuses[new_pipeline_id]["Первичный контакт"]
                        data_patch_leads = [{'id': lead['id'],
                                             'pipeline_id': new_pipeline_id,
                                             'status_id': new_status_id,
                                             },
                                            ]
                        result = await self.amo_client.patch_leads(json_data=data_patch_leads)
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