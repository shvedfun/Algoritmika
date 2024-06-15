import datetime
import logging


import ydb
from api.public.algv2.models import Contact, Booking
from api.utils.logger import get_logger

logging.getLogger('ydb').setLevel(logging.INFO)
logger = get_logger(__name__)


class DBProvider:
  def __init__(self) -> None:
    self.__driver = ydb.Driver(
        endpoint='grpcs://ydb.serverless.yandexcloud.net:2135',
        # database='/ru-central1/b1g8ckg2m6u5aund7adt/etngps57384okpq145s3',
        # credentials=ydb.iam.ServiceAccountCredentials.from_file('creds/algoritmika_sa.key'),
        database='/ru-central1/b1ghrn4mjhc680ge5mpc/etn6596chmgkqkfld3rf',
        credentials=ydb.iam.ServiceAccountCredentials.from_file('creds/algo-service-account authorized key.json'),
    )

  def __execute_query(self, session, query, params):
    logger.debug(f'params = {params}')
    return session.transaction().execute(
        query,
        params,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
    )

  def execute_query(self, query, params=None):
    self.__driver.wait(fail_fast=True, timeout=5)
    with ydb.SessionPool(self.__driver) as pool:
      result = pool.retry_operation_sync(
          lambda x: self.__execute_query(x, query, params=params))
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

    def get_contact_id_by_phone(self, phone):
        sql = f'SELECT id FROM i_client WHERE phone = {phone} order by id desc'
        result = self.db.execute_query(sql)[0].rows
        return result[0][0] if result else None

    def upsert_booking(bk: Booking):
        sql = f'UPSERT INTO i_booking (student_id, group_id, status, created, updated) VAlUES ' \
              f'(\'{bk.student_id}\', {bk.group_id}, \'{bk.status}\'' \
              f', CAST(\'{bk.created.isoformat()}\' AS DateTime), CAST(\'{bk.updated.isoformat()}\' AS DateTime))'
        logger.debug(f'sql = {sql}')
        db.execute_query(sql)

    def get_booking(self, student_id: str = None, group_id: int = None):
        sql = 'SELECT * FROM i_booking WHERE 1=1'
        if student_id:
            sql += f' AND student_id={student_id}'
        if group_id:
            sql += f' AND group_id={group_id}'
        sql += ' ORDER BY id'
        result = db.execute_query(sql)[0].rows
        return result

    def get_contact(self, contact_id):
        logger.debug(f'contact_id = {contact_id}')
        sql = """
        DECLARE $contact_id AS Uint64;
        
        SELECT * FROM i_contact WHERE 1=1
        """
        if contact_id:
            sql += f' AND id = {contact_id}'
        result = db.execute_query(sql, params={'$contact_id': contact_id})[0].rows
        return result
    


db_executor = DBExecutor(db=db)


if __name__ == '__main__':
  DBProvider().test()

