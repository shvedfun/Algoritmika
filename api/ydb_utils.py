import datetime
import json
import logging
import uuid


import ydb
from api.public.algv2.models import Contact, Booking, Message, Student
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
        sql = f'UPSERT INTO i_contact (id, amo_id, amo_lead_id, name, first_name, last_name, phone, created, params) VALUES ' \
              f'({c.id}, {c.amo_id}, {c.amo_lead_id}, \'{c.name}\', \'{c.first_name}\', \'{c.last_name}\', \'{c.phone}\', CAST(\'{c.created}\' AS DateTime), \'{json.dumps(c.params)}\')'
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
        sql = f'SELECT id FROM i_contact WHERE phone = \'{phone}\' ORDER BY id DESC'
        result = self.db.execute_query(sql)[0].rows
        return result[0][0] if result else None

    def upsert_booking(self, bk: Booking):
        sql = f'UPSERT INTO i_booking (student_id, group_id, status, created, updated) VAlUES ' \
              f'(\'{bk.student_id}\', {bk.group_id}, \'{bk.status}\'' \
              f', CAST(\'{bk.created.isoformat()}\' AS DateTime), CAST(\'{bk.updated.isoformat()}\' AS DateTime))'
        logger.debug(f'sql = {sql}')
        db.execute_query(sql)

    def get_booking(self, student_id: str = None, group_id: int = None):
        sql = 'SELECT * FROM i_booking WHERE 1=1'
        if student_id:
            sql += f' AND student_id= \'{student_id}\''
        if group_id:
            sql += f' AND group_id={group_id}'
        # sql += ' ORDER BY id'
        logger.debug(f'sql = sql')
        result = db.execute_query(sql)[0].rows
        return result

    def get_contact(self, contact_id=None, phone: str=""):
        logger.debug(f'contact_id = {contact_id}, phone = {phone}')
        params = {}
        sql = """
        SELECT * FROM i_contact WHERE 1=1
        """
        if contact_id:
            params['contact_id'] = contact_id
            sql += f' AND id = {contact_id}'
        if phone:
            sql += f' AND phone = \'{phone}\''
        sql += " ORDER BY id DESC"
        logger.debug(f'sql = {sql}')
        result = db.execute_query(sql)[0].rows
        logger.debug(f'contact_result = {result}')
        return result

    def insert_message(self, ms: Message):
        # if not ms.id:
        ms.id = str(uuid.uuid4())
        # ms.created = datetime.datetime.now(tz=datetime.timezone.utc)
        sql = f'INSERT INTO i_message (id, text, ai_id, contact_id, created) VALUES (\'{ms.id}\', \'{ms.text}\', \'{ms.ai_id}\', {ms.contact_id}, CAST({int(ms.created.timestamp() * 10**6)} AS Timestamp))'
        logger.debug(f'sql = {sql}')
        result = db.execute_query(sql)
        sql = f'SELECT * FROM i_message WHERE id = \'{ms.id}\''
        result = db.execute_query(sql)[0].rows[0]
        result['created'] = (result['created']// 10**6)
        result = Message(**result)
        return result

    def get_student(self, student_id: str=None) -> Student:
        sql = f'SELECT * FROM i_student'
        if student_id is not None:
            sql += f' WHERE id = \'{student_id}\' ORDER BY id DESC'
        logger.debug(f'sql = {sql}')
        result = db.execute_query(sql)[0].rows
        if len(result) > 0:
            result = result[0]
            result = Student(**result)
        else:
            result = None
        return result

    def get_lead_id_from_contact_id(self, contact_id) -> int | None:
        lead_id = None
        contact = self.get_contact(contact_id=contact_id)
        logger.debug(f'contact = {contact}')
        if contact:
            contact = contact[0]
            lead_id = contact.get('amo_lead_id')
        logger.debug(f"lead_id = {lead_id}")
        return lead_id


    def get_lead_id_from_student_id(self, student_id) -> int:
        lead_id = None
        student = self.get_student(student_id)
        logger.debug(f'student = {student}')
        contact = None
        if student.contact_id:
            contact = self.get_contact(contact_id=student.contact_id)
        logger.debug(f'contact = {contact}')
        if contact:
            contact = contact[0]
            lead_id = contact.get('amo_lead_id')
        logger.debug(f"lead_id = {lead_id}")
        return lead_id

    def get_school(self, school_id=None, school_number=None):
        sql = 'SELECT * FROM i_school WHERE 1 = 1 '
        if school_id is not None:
            sql += f' AND id = {school_id} '
        if school_number is not  None:
            sql += f' AND number = {int(school_number)}'
        result = db.execute_query(sql)[0].rows
        return result


db_executor = DBExecutor(db=db)


if __name__ == '__main__':
  DBProvider().test()

