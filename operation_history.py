from datetime import datetime
from typing import Optional
import requests

from exceptions import IllegalParamType, IllegalParamStartRecord, IllegalParamRecords, IllegalParamLabel, IllegalParamFromDate, IllegalParamTillDate, TechnicalError

class Operation:
    '''
    Задаёт поля для операций.
    '''
    def __init__(self,
                 operation_id: str = None, # Идентификатор операции
                 status: str = None, # Статус платежа/перевода (success, refused, in_progress)
                 datetime: Optional[datetime] = None, # Дата и время совершения операции
                 title: str = None, # Краткое описание операции (название магазина или источник пополнения)
                 pattern_id: str = None, # Идентификатор шаблона, по которому совершен платеж. Присутствует только для платежей
                 direction: str = None, # Направление движения средств (in, out)
                 amount: float = None, # Сумма операции
                 label: str = None, # Метка платежа. Присутствует для входящих и исходящих переводов другим пользователям ЮMoney, у которых был указан параметр label вызова request-payment
                 type: str = None, # Тип операции (payment-shop, outgoing-transfer, deposition, incoming-transfer)
                 ):
        self.operation_id = operation_id
        self.status = status
        self.datetime = datetime
        self.title = title
        self.pattern_id = pattern_id
        self.direction = direction
        self.amount = amount
        self.label = label
        self.type = type

class History:
    '''
    Метод позволяет просматривать историю операций (полностью или частично) в постраничном режиме.\n
    Записи истории выдаются в обратном хронологическом порядке: от последних к более ранним.
    '''
    def __init__(self,
                 base_url: str = None,
                 token: str = None,
                 method: str = None,
                 type: str = None, # Перечень типов операций, которые требуется отобразить (depositition, payment)
                 label: str = None, # Отбор платежей по значению метки. Выбираются платежи, у которых указано заданное значение параметра label
                 from_date: Optional[datetime] = None, # Вывести операции от момента времени (операции, равные from, или более поздние). Если параметр отсутствует, выводятся все операции
                 till_date: Optional[datetime] = None, # Вывести операции до момента времени (операции более ранние, чем till). Если параметр отсутствует, выводятся все операции
                 start_record: str = None, # Если параметр присутствует, то будут отображены операции, начиная с номера start_record. Операции нумеруются с 0
                 records: int = None, # Количество запрашиваемых записей истории операций. Допустимые значения: от 1 до 100
                 details: bool = None, # Показывать подробные детали операции
                 ):

        self.__private_method = method
        self.__private_base_url = base_url
        self.__private_token = token

        self.type = type
        self.label = label
        try:
            if from_date is not None:
                from_date = '{Y}-{m}-{d}T{H}:{M}:{S}'.format(
                    Y=str(from_date.year),
                    m=str(from_date.month),
                    d=str(from_date.day),
                    H=str(from_date.hour),
                    M=str(from_date.minute),
                    S=str(from_date.second)
                )
        except:
            raise IllegalParamFromDate()

        try:
            if till_date is not None:
                till_date = '{Y}-{m}-{d}T{H}:{M}:{S}'.format(
                    Y=str(till_date.year),
                    m=str(till_date.month),
                    d=str(till_date.day),
                    H=str(till_date.hour),
                    M=str(till_date.minute),
                    S=str(till_date.second)
                )
        except:
            IllegalParamTillDate()

        self.from_date = from_date
        self.till_date = till_date
        self.start_record = start_record
        self.records = records
        self.details = details

        data = self._request()

        if 'error' in data:
            if data['error'] == 'illegal_param_type':
                raise IllegalParamType()
            elif data['error'] == 'illegal_param_start_record':
                raise IllegalParamStartRecord()
            elif data['error'] == 'illegal_param_records':
                raise IllegalParamRecords()
            elif data['error'] == 'illegal_param_label':
                raise IllegalParamLabel()
            elif data['error'] == 'illegal_param_from':
                raise IllegalParamFromDate()
            elif data['error'] == 'illegal_param_till':
                raise IllegalParamTillDate()
            else:
                raise TechnicalError()


        self.next_record = None
        if 'next_record' in data:
            self.next_record = data['next_record']

        self.operations = list()
        for operation_data in data['operations']:
            param = {}
            if 'operation_id' in operation_data:
                param['operation_id'] = operation_data['operation_id']
            else:
                param['operation_id'] = None
            if 'status' in operation_data:
                param['status'] = operation_data['status']
            else:
                param['status'] = None
            if 'datetime' in operation_data:
                param['datetime'] = datetime.strptime(str(operation_data['datetime']).replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')
            else:
                param['datetime'] = None
            if 'title' in operation_data:
                param['title'] = operation_data['title']
            else:
                param['title'] = None
            if 'pattern_id' in operation_data:
                param['pattern_id'] = operation_data['pattern_id']
            else:
                param['pattern_id'] = None
            if 'direction' in operation_data:
                param['direction'] = operation_data['direction']
            else:
                param['direction'] = None
            if 'amount' in operation_data:
                param['amount'] = operation_data['amount']
            else:
                param['amount'] = None
            if 'label' in operation_data:
                param['label'] = operation_data['label']
            else:
                param['label'] = None
            if 'type' in operation_data:
                param['type'] = operation_data['type']
            else:
                param['type'] = None


            operation = Operation(
                operation_id= param['operation_id'],
                status=param['status'],
                datetime=datetime.strptime(str(param['datetime']).replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S'),
                title=param['title'],
                pattern_id=param['pattern_id'],
                direction=param['direction'],
                amount=param['amount'],
                label=param['label'],
                type=param['type'],
            )
            self.operations.append(operation)



    def _request(self):

        access_token = str(self.__private_token)
        url = self.__private_base_url + self.__private_method

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {}
        if self.type is not None:
            payload['type'] = self.type
        if self.label is not None:
            payload['label'] = self.label
        if self.from_date is not None:
            payload['from'] = self.from_date
        if self.till_date is not None:
            payload['till'] = self.till_date
        if self.start_record is not None:
            payload['start_record'] = self.start_record
        if self.records is not None:
            payload['records'] = self.records
        if self.details is not None:
            payload['details'] = self.details

        response = requests.request('POST', url, headers=headers, data=payload)

        return response.json()