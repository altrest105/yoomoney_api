import requests
from exceptions import InvalidToken

class BalanceDetails:
    '''
    Задаёт поля для детального баланса.
    '''
    def __init__(self,
                 total: float = None, # Общий баланс счета
                 available: float = None, # Сумма доступная для расходных операций
                 deposition_pending: float = None, # Сумма стоящих в очереди пополнений. Если зачислений в очереди нет, то параметр отсутствует
                 blocked: float = None, # Сумма заблокированных средств по решению исполнительных органов. Если заблокированных средств нет то параметр отсутствует
                 debt: float = None, # Сумма задолженности (отрицательного остатка на счете). Если задолженности нет, то параметр отсутствует
                 hold: float = None, # Сумма замороженных средств. Если замороженных средств нет, то параметр отсутствует
                 ):

        self.total = total
        self.available = available
        self.deposition_pending = deposition_pending
        self.blocked = blocked
        self.debt = debt
        self.hold = hold

class Card:
    '''
    Задаёт поля для карт.
    '''
    def __init__(self,
                 pan_fragment: str = None, # Маскированный номер карты
                 type: str = None, # Тип карты. Может отсутствовать, если неизвестен (VISA, MasterCard, AmericanExpress, JCB)
                 ):
        self.pan_fragment = pan_fragment
        self.type = type

class Account:
    '''
    Получение информации о состоянии счета пользователя.
    '''
    def __init__(self,
                 base_url: str = None,
                 token: str = None,
                 method: str = None,
                 ):

        self.__private_method = method
        self.__private_base_url = base_url
        self.__private_token = token

        data = self._request()

        if len(data) != 0:
            self.account = data['account'] # Номер счета пользователя
            self.balance = data['balance'] # Баланс счета пользователя
            self.currency = data['currency'] #Код валюты счета пользователя. Всегда 643 (рубль РФ по стандарту ISO 4217)
            self.account_status = data['account_status'] # Статус пользователя (anonymous, named, identified)
            self.account_type = data['account_type'] # Тип счета пользователя (personal, professional)

            self.balance_details = BalanceDetails() # По умолчанию этот блок отсутствует. Блок появляется, если сейчас или когда-либо ранее были зачисления в очереди, задолженности, блокировки средств.
            if 'balance_details' in data:
                if 'available' in data['balance_details']:
                    self.balance_details.available = float(data['balance_details']['available'])
                if 'blocked' in data['balance_details']:
                    self.balance_details.blocked = float(data['balance_details']['blocked'])
                if 'debt' in data['balance_details']:
                    self.balance_details.debt = float(data['balance_details']['debt'])
                if 'deposition_pending' in data['balance_details']:
                    self.balance_details.deposition_pending = float(data['balance_details']['deposition_pending'])
                if 'total' in data['balance_details']:
                    self.balance_details.total = float(data['balance_details']['total'])
                if 'hold' in data['balance_details']:
                    self.balance_details.hold = float(data['balance_details']['hold'])

            self.cards_linked = [] # Информация о привязанных банковских картах. Если к счету не привязано ни одной карты, параметр отсутствует. 
            if 'cards_linked' in data:
                for card_linked in data['cards_linked']:
                    card = Card(pan_fragment=card_linked['pan_fragment'], type=card_linked['type'])
                    self.cards_linked.append(card)
        else:
            raise InvalidToken()

    def _request(self):

        access_token = str(self.__private_token)
        url = self.__private_base_url + self.__private_method

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request('POST', url, headers=headers)

        return response.json()