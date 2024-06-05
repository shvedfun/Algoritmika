import datetime
import logging


import ydb
from api.public.algv2.models import Contact
from api.utils.logger import logger_config

logging.getLogger('ydb').setLevel(logging.INFO)
logger = logger_config(__name__)


class DBProvider:
  def __init__(self) -> None:
    self.__driver = ydb.Driver(
        endpoint='grpcs://ydb.serverless.yandexcloud.net:2135',
        # database='/ru-central1/b1g8ckg2m6u5aund7adt/etngps57384okpq145s3',
        # credentials=ydb.iam.ServiceAccountCredentials.from_file('creds/algoritmika_sa.key'),
        database='/ru-central1/b1ghrn4mjhc680ge5mpc/etn6596chmgkqkfld3rf',
        credentials=ydb.iam.ServiceAccountCredentials.from_file('creds/algo-service-account authorized key.json'),
    )

  def __execute_query(self, session, query):
    return session.transaction().execute(
        query,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
    )

  def execute_query(self, query):
    self.__driver.wait(fail_fast=True, timeout=5)
    with ydb.SessionPool(self.__driver) as pool:
      result = pool.retry_operation_sync(
          lambda x: self.__execute_query(x, query))
    return result

  def test(self):
    print(self.execute_query('select * from queue;'))

db = DBProvider()


class DBExecutor:

    def __init__(self, db: DBProvider):
        self.db = db

    def upsert_contact_from_amo(self, contact_amo):
        c = Contact(**contact_amo)
        c.amo_id = c.id
        c.created = datetime.datetime.utcnow().isoformat()
        # c.id = str(uuid.uuid4())
        sql = f'UPSERT INTO i_contact (id, amo_id, name, first_name, last_name, phone, created) VALUES ' \
              f'({c.id}, {c.amo_id}, \'{c.name}\', \'{c.first_name}\', \'{c.last_name}\', \'{c.phone}\', CAST(\'{c.created}\' AS DateTime))'
        logger.debug(f'sql = {sql}')
        result = db.execute_query(sql)

    def get_group(self, id):
        sql = f'SELECT * FROM i_group WHERE id = {id}'
        result = self.db.execute_query(sql)[0].rows
        return result[0] if result else result

    def get_number_booking(self, group_id):
        sql = f'SELECT COUNT(*) FROM i_booking WHERE group_id = {group_id}'
        result = self.db.execute_query(sql)[0].rows
        return result[0][0] if result else -1

db_connector = DBExecutor(db=db)


if __name__ == '__main__':
  DBProvider().test()

