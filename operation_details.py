from datetime import datetime
from typing import List
import requests

from exceptions import IllegalParamOperationId, TechnicalError

class DigitalProduct:
    '''
    При успешном платеже в магазин цифровых товаров в ответе присутствует поле digital_goods, которое содержит список товаров и список бонусов.
    '''
    def __init__(self,
                 merchant_article_id: str, # Идентификатор товара в системе продавца. Присутствует только для товаров
                 serial: str, # Серийный номер товара (открытая часть пин-кода, кода активации или логин)
                 secret: str # Секрет цифрового товара (закрытая часть пин-кода, кода активации, пароль или ссылка на скачивание)
                 ):
        self.merchant_article_id = merchant_article_id
        self.serial = serial
        self.secret = secret

class DigitalBonus:
    '''
    Вспомогательный класс для поля digital_goods
    '''
    def __init__(self,
                 serial: str, # Серийный номер товара (открытая часть пин-кода, кода активации или логин)
                 secret: str # Секрет цифрового товара (закрытая часть пин-кода, кода активации, пароль или ссылка на скачивание)
                 ):
        self.serial = serial
        self.secret = secret

class DigitalGood:
    '''
    Вспомогательный класс для поля digital_goods
    '''
    def __init__(self,
                 products: List[DigitalProduct],
                 bonuses: List[DigitalBonus]
                 ):
        self.products = products
        self.bonuses = bonuses


class Details:
    '''
    Позволяет получить детальную информацию об операции из истории.
    '''
    def __init__(self,
                 base_url: str,
                 token: str,
                 operation_id: str, # Идентификатор операции. Значение параметра следует указывать как значение параметра operation_id ответа метода operation-history или значение поля payment_id ответа метода process-payment, если запрашивается история счета плательщика
                 method: str = None,
                 ):
        self.__private_method = method
        self.__private_token = token
        self.__private_base_url = base_url
        self.operation_id = operation_id

        data = self._request()

        if 'error' in data:
            if data['error'] == 'illegal_param_operation_id':
                raise IllegalParamOperationId()
            else:
                raise TechnicalError()

        self.status = None # Статус платежа (перевода). Значение параметра соответствует значению поля status ответа метода operation-history
        self.pattern_id = None # Статус платежа (перевода). Значение параметра соответствует значению поля status ответа метода operation-history
        self.direction = None # Направление движения средств (in, out)
        self.amount = None # Сумма операции (сумма списания со счета)
        self.amount_due = None # Сумма к получению. Присутствует для исходящих переводов другим пользователям
        self.fee = None # Сумма комиссии. Присутствует для исходящих переводов другим пользователям
        self.datetime = None # Дата и время совершения операции
        self.title = None # Краткое описание операции (название магазина или источник пополнения)
        self.sender = None # Номер счета отправителя перевода. Присутствует для входящих переводов от других пользователей
        self.recipient = None # Идентификатор получателя перевода. Присутствует для исходящих переводов другим пользователям
        self.recipient_type = None # Тип идентификатора получателя перевода (account, phone, email). Присутствует для исходящих переводов другим пользователям
        self.message = None # Сообщение получателю перевода. Присутствует для переводов другим пользователям
        self.comment = None # Комментарий к переводу или пополнению. Присутствует в истории отправителя перевода или получателя пополнения
        self.label = None # Метка платежа. Присутствует для входящих и исходящих переводов другим пользователям ЮMoney, у которых был указан параметр label вызова request-payment
        self.details = None # Детальное описание платежа. Строка произвольного формата, может содержать любые символы и переводы строк. Необязательный параметр
        self.type = None # Тип операции. Описание возможных типов операций см. в описании метода operation-history
        self.digital_goods = None # Данные о цифровом товаре (пин-коды и бонусы игр, iTunes, Xbox, etc.) Поле присутствует при успешном платеже в магазины цифровых товаров

        if 'status' in data:
            self.status = data['status']
        if 'pattern_id' in data:
            self.pattern_id = data['pattern_id']
        if 'direction' in data:
            self.direction = data['direction']
        if 'amount' in data:
            self.amount = data['amount']
        if 'amount_due' in data:
            self.amount_due = data['amount_due']
        if 'fee' in data:
            self.fee = data['fee']
        if 'datetime' in data:
            self.datetime = datetime.strptime(str(data['datetime']).replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')
        if 'title' in data:
            self.title = data['title']
        if 'sender' in data:
            self.sender = data['sender']
        if 'recipient' in data:
            self.recipient = data['recipient']
        if 'recipient_type' in data:
            self.recipient_type = data['recipient_type']
        if 'message' in data:
            self.message = data['message']
        if 'comment' in data:
            self.comment = data['comment']
        if 'label' in data:
            self.label = data['label']
        if 'details' in data:
            self.details = data['details']
        if 'type' in data:
            self.type = data['type']
        if 'digital_goods' in data:
            products: List[DigitalProduct] = []
            for product in data['digital_goods']['article']:
                digital_product = DigitalProduct(merchant_article_id=product['merchantArticleId'],
                                                 serial=product['serial'],
                                                 secret=product['secret'],
                                                 )
                products.append(digital_product)

            bonuses: List[DigitalBonus] = []
            for bonus in data['digital_goods']['bonus']:
                digital_product = DigitalBonus(serial=bonus['serial'],
                                               secret=bonus['secret'],
                                               )
                bonuses.append(digital_product)

            self.digital_goods = DigitalGood(products=products,
                                             bonuses=bonuses
                                             )

    def _request(self):

        access_token = str(self.__private_token)
        url = self.__private_base_url + self.__private_method

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {}

        payload['operation_id'] = self.operation_id


        response = requests.request('POST', url, headers=headers, data=payload)

        return response.json()
