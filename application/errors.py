"""
Ошибки
"""


class IncorrectDataReceivedError(Exception):
    """
    Исключение - получены некорректные данные от сокета
    """

    def __str__(self):
        return 'Принято некорректное сообщение от удаленного компьютера'


class NonDictInputError(Exception):
    """
    Исключение - аргумент функции не является словарем
    """

    def __str__(self):
        return 'Аргумент функции должен быть словарем'


class ReqFieldMissingError(Exception):
    """
    Исключение - отсутствует обязательное поле в принятом словаре
    """

    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}'
