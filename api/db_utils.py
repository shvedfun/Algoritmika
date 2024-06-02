import logging

import ydb

logging.getLogger('ydb').setLevel(logging.INFO)


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

if __name__ == '__main__':
  DBProvider().test()

