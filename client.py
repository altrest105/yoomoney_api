from datetime import datetime

from account_info import Account
from operation_history import History
from operation_details import Details


class Client:
    '''
    Интерфейс взаимодействия с аккаунтом.
    '''
    def __init__(self,
                 token: str = None,
                 base_url: str = None,
                 ):

        if base_url is None:
            self.base_url = 'https://yoomoney.ru/api/'

        if token is not None:
            self.token = token

    def account_info(self):
        method = 'account-info'
        return Account(base_url=self.base_url,
                       token=self.token,
                       method=method
                       )

    def operation_history(self,
                          type: str = None,
                          label: str = None,
                          from_date: datetime = None,
                          till_date: datetime = None,
                          start_record: str = None,
                          records: int = None,
                          details: bool = None,
                          ):
        method = 'operation-history'
        return History(base_url=self.base_url,
                       token=self.token,
                       method=method,
                       type=type,
                       label=label,
                       from_date=from_date,
                       till_date=till_date,
                       start_record=start_record,
                       records=records,
                       details=details,
                       )

    def operation_details(self,
                          operation_id: str
                          ):
        method = 'operation-details'
        return Details(base_url=self.base_url,
                       token=self.token,
                       method=method,
                       operation_id=operation_id,
                       )