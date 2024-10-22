import requests
from typing import List

from exceptions import InvalidRequest, InvalidScope, UnauthorizedClient, AccessDenied, InvalidGrant, EmptyToken

class Authorize:
    '''
    Авторизация приложения.
    '''
    def __init__(
            self,
            client_id: str, # Идентификатор приложения, полученный при регистрации\
            redirect_uri: str, # URI, на который сервер OAuth передает результат авторизации (совпадает с указанным при регистрации)
            scope: List[str], # Список запрашиваемых прав (account-info, operation-history, operation-details, payment, payment-shop, payment-p2p, money-source)
            client_secret: str = None # Секретное слово для проверки подлинности приложения (необязателен)
            ):

        # Запрос авторизации
        url = 'https://yoomoney.ru/oauth/authorize?client_id={client_id}&response_type=code' \
              '&redirect_uri={redirect_uri}&scope={scope}'.format(client_id=client_id,
                                                                  redirect_uri=redirect_uri,
                                                                  scope='%20'.join([str(elem) for elem in scope]))

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request('POST', url, headers=headers)

        if response.status_code == 200:
            print('Перейдите на данный сайт и подтвердите авторизацию:')
            print(response.url)
        elif 'error' in response.json():
            error = response.json()['error']
            if error == 'invalid_request':
                raise InvalidRequest()
            elif error == 'invalid_scope':
                raise InvalidScope()
            elif error == 'unauthorized_client':
                raise UnauthorizedClient()
            elif error == 'access_denied':
                raise AccessDenied()

        # Получение токена
        code = str(input('Введите redicted_uri (https://yourredirect_uri?code=XXXXXXXXXXXXX) или просто код: '))
        try:
            code = code[code.index('code=') + 5:].replace(' ','')
        except:
            pass

        if not(client_id):
            url = 'https://yoomoney.ru/oauth/token?code={code}&client_id={client_id}&' \
                'grant_type=authorization_code&redirect_uri={redirect_uri}'.format(code=str(code),client_id=client_id, redirect_uri=redirect_uri)
        else:
            url = 'https://yoomoney.ru/oauth/token?code={code}&client_id={client_id}&' \
                'grant_type=authorization_code&redirect_uri={redirect_uri}&client_secret={client_secret}'.format(code=str(code),client_id=client_id, redirect_uri=redirect_uri, client_secret=client_secret)

        response = requests.request('POST', url, headers=headers)

        if 'error' in response.json():
            error = response.json()['error']
            if error == 'invalid_request':
                raise InvalidRequest()
            elif error == 'unauthorized_client':
                raise UnauthorizedClient()
            elif error == 'invalid_grant':
                raise InvalidGrant()

        if response.json()['access_token'] == '':
            raise EmptyToken()

        print('Ваш код доступа:')
        print(response.json()['access_token'])