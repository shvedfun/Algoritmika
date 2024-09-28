import asyncio
import json
import traceback

from amo_utils.client import AMOClient, pipelines
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
            sleep_new_contact: int = 30
    ) -> None:
        self.sleep_time = sleep_time
        self.sleep_new_contact = sleep_new_contact
        self.sleep_contact2ai_message = sleep_contact2ai_message
        self.sleep_ai2contact_message = sleep_ai2contact_message
        # self.amo_client = amo_client or AMOClient(
        #     url_prefix= settings.AMO_URL,
        #     long_token= settings.AMO_TOKEN,
        # )
        self.aiclient = ai_client or AIClient(url=settings.AI_URL, token=settings.AI_TOKEN)

    async def run(self):
        count = 0
        while True:
            try:
                if not settings.IS_LOCAL:
                    if count % self.sleep_contact2ai_message == 0:
                        pass
                        # await self.do_contact2ai_message()
                    if count % self.sleep_ai2contact_message == 0:
                        pass
                        # await self.do_ai2contact_message()
                    if count % self.sleep_new_contact == 0:
                        await self.do_new_lead()
                else:
                    if count % 100 == 0:
                        logger.debug(f'Работаю d LOCAL окружении -> не вызываю функции background')
            except Exception as e:
                logger.error(f'Error {e} - {traceback.format_exc()}')
            finally:
                await asyncio.sleep(self.sleep_time)
                count += 1


    async def do_new_lead(self):
        for partner, params in settings.partners.items():
            amo_client = AMOClient(
                url_prefix= params["AMO_URL"],
                long_token= params["AMO_TOKEN"],
                pipelines=params["pipelines"],
                pipelines_statuses=params["pipelines_statuses"],
            )
            logger.info('partner %r', partner)
            await self._do_new_lead(amo_client, partner)



    async def _do_new_lead(self, amo_client: AMOClient, partner):
        pipeline_id = amo_client.pipelines_get('default')
        logger.debug('amo_client.pipelines = %r', amo_client.pipelines)
        result = await amo_client.get_leads(pipeline_id=pipeline_id)
        if result:
            logger.debug(f'result get leads = {result}')
        leads = amo_client.get_leads_from_response(result)
        schools = db_executor.get_school()
        for lead in leads:
            logger.debug(f'schools = {schools}')
            if lead.get('status_id', 0) == amo_client.pipelines_statuses[str(pipeline_id)]["Первичный контакт"]:
                contacts = AMOClient.get_contact_ids_from_dict_lead(lead)
                main_contact_id = amo_client.get_main_contact_id(contacts)
                logger.debug(f'main_contact_id = {main_contact_id}')
                if main_contact_id:
                    contact = await amo_client.get_contact(main_contact_id)
                    validated_contact = amo_client.get_validated_contact(contact, lead, schools, partner)
                    logger.info(f'validated_contact = {validated_contact}')
                    if validated_contact['phone']:
                        db_executor.upsert_contact_from_amo(validated_contact)
                        new_pipeline_id = amo_client.pipelines_get('AI')
                        new_status_id = amo_client.pipelines_statuses[str(new_pipeline_id)]["Первичный контакт"]
                        data_patch_leads = [{'id': lead['id'],
                                             'pipeline_id': new_pipeline_id,
                                             'status_id': new_status_id,
                                             },
                                            ]
                        logger.debug(f'data_patch_leads = {data_patch_leads}')
                        result = await amo_client.patch_leads(json_data=data_patch_leads)
                        # logger.debug(f'result = {result}')
                        ai_result = await self.aiclient.send_newcontact2ai(validated_contact)

                    else:
                        new_pipeline_id = amo_client.pipelines_get('Human')
                        new_status_id = amo_client.pipelines_statuses[new_pipeline_id]["Первичный контакт"]
                        data_patch_leads = [{'id': lead['id'],
                                             'pipeline_id': new_pipeline_id,
                                             'status_id': new_status_id,
                                             },
                                            ]
                        result = await amo_client.patch_leads(json_data=data_patch_leads)
                        # move_lead_

        if result:
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