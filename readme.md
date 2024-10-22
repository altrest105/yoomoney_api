# Описание
Обновлённое API для yoomoney

---

# Пример программы
'''python
from authorization import Authorize
from client import Client
from quickpay import Quickpay

Authorize( # Авторизация
      client_id='your_client_id', # client_id из зарегистированного приложения
      redirect_uri='your_uri', # URI
      scope=['account-info',
             'operation-history',
             'operation-details',
             'incoming-transfers',
             'payment-shop',
             ]
      )


TOKEN = 'token' # Вставляем полученный токен из авторизации

client = Client(TOKEN)
user = client.account_info()
account_id = user.account

quickpay = Quickpay( # Создание ссылки для оплаты
            receiver=f'{account_id}', # Номер аккаунта
            quickpay_form='shop',
            paymentType='AC', # Способ оплаты банковской картой
            sum=10, # Сумма оплаты
            label='test' # Комментарий для проверки на наличие оплаты
            )

print(quickpay.base_url)


history = client.operation_history(label='test') # Просмотр истории транзакций по label

if history.operations == []:
    print('Оплата не найдена!')

for operation in history.operations:
    if operation.status == 'success':
        print('Оплата найдена!')
'''
