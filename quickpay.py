import requests

class Quickpay:
    '''
    Создание ссылки для оплаты.
    '''
    def __init__(self,
                 receiver: str, # Номер кошелька ЮMoney, на который нужно зачислять деньги отправителей
                 quickpay_form : str, # Тип формы. Фиксированное значение — button
                 paymentType: str, # Способ оплаты (PC, AC)
                 sum: float, # Сумма перевода (спишется с отправителя)
                 label: str = None, # Метка, которую сайт или приложение присваивает конкретному переводу. Например, в качестве метки можно указывать код или идентификатор заказа
                 successURL: str = None, # URL-адрес для редиректа после совершения перевода
                 ):
        self.receiver = receiver
        self.quickpay_form = quickpay_form
        self.paymentType = paymentType
        self.sum = sum
        self.label = label
        self.successURL = successURL

        self.response = self._request()

    def _request(self):

        self.base_url = 'https://yoomoney.ru/quickpay/confirm.xml?'

        payload = {}

        payload['receiver'] = self.receiver
        payload['quickpay_form'] = self.quickpay_form
        payload['paymentType'] = self.paymentType
        payload['sum'] = self.sum

        if self.label != None:
            payload['label'] = self.label
        if self.successURL != None:
            payload['successURL'] = self.successURL

        for value in payload:
            self.base_url+=str(value).replace('_','-') + '=' + str(payload[value])
            self.base_url+='&'

        self.base_url = self.base_url[:-1].replace(' ', '%20')

        response = requests.request('POST', self.base_url)

        self.redirected_url = response.url
        return response