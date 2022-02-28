"""
Декораторы для приложения клиент-сервер
"""
import inspect
import logging
import sys


if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func):
    """
    Декоратор для логгирования, фиксирующий обращение к декорируемой функции
    :param func: Декорируемая функция
    :return:
    """
    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func.__name__} с параметрами {args}, {kwargs}. '
                     f'Вызов выполнен из модуля {func.__module__}. '
                     f'Вызов выполнен из функции {inspect.stack()[1][3]}.')
        return res
    return decorated
