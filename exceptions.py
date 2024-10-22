class YooMoneyError(Exception):
    '''Базовый класс'''

class InvalidRequest(YooMoneyError):
    message = 'Обязательные параметры запроса отсутствуют или имеют некорректные или недопустимые значения.'
    def __init__(self, ):
        super().__init__(self.message)

class InvalidScope(YooMoneyError):
    message = 'Параметр scope отсутствует, либо имеет некорректное значение или имеет логические противоречия.'
    def __init__(self, ):
        super().__init__(self.message)

class UnauthorizedClient(YooMoneyError):
    message = 'Неверное значение параметра client_id или client_secret, либо приложение не имеет права запрашивать авторизацию (например, ЮMoney заблокировали его client_id).'
    def __init__(self, ):
        super().__init__(self.message)

class AccessDenied(YooMoneyError):
    message = 'Пользователь отклонил запрос авторизации приложения.'
    def __init__(self, ):
        super().__init__(self.message)

class InvalidScope(YooMoneyError):
    message = 'Параметр scope отсутствует, либо имеет некорректное значение или имеет логические противоречия.'
    def __init__(self, ):
        super().__init__(self.message)

class InvalidGrant(YooMoneyError):
    message = 'В выдаче access_token отказано. ЮMoney не выдавали временный токен, токен просрочен, или по этому временному токену уже выдан access_token (повторный запрос токена авторизации с тем же временным токеном).'
    def __init__(self, ):
        super().__init__(self.message)

class EmptyToken(YooMoneyError):
    message = 'Токен пустой, процедуру авторизации следует повторить сначала.'
    def __init__(self, ):
        super().__init__(self.message)

class InvalidToken(YooMoneyError):
    message = 'Неправильный токен, либо токен не имеет требуемых прав.'
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamType(YooMoneyError):
    message = 'Неверное значение параметра type.'
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamStartRecord(YooMoneyError):
    message = 'Неверное значение параметра start_record'
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamRecords(YooMoneyError):
    message = 'Неверное значение параметра records'
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamLabel(YooMoneyError):
    message = 'Неверное значение параметра label'
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamFromDate(YooMoneyError):
    message = '	Неверное значение параметра from'
    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamTillDate(YooMoneyError):
    message = 'Неверное значение параметра till'
    def __init__(self, ):
        super().__init__(self.message)

class TechnicalError(YooMoneyError):
    message = 'Техническая ошибка, повторите вызов операции позднее'
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamOperationId(YooMoneyError):
    message = 'Неверное значение параметра operation_id'
    def __init__(self, ):
        super().__init__(self.message)