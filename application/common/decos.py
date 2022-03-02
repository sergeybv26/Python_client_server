"""
Декораторы для приложения клиент-сервер
"""
import inspect
import logging
import socket
import sys

sys.path.append('../')
import log.client_log_config
import log.server_log_config

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func):
    """
    Декоратор для логгирования, фиксирующий обращение к декорируемой функции
    :param func: Декорируемая функция
    :return: None
    """

    def decorated(*args, **kwargs):
        res = func(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func.__name__} с параметрами {args}, {kwargs}. '
                     f'Вызов выполнен из модуля {func.__module__}. '
                     f'Вызов выполнен из функции {inspect.stack()[1][3]}.')
        return res

    return decorated


def login_required(func):
    """
    Декоратор, который проверяет, что клиент авторизован на сервере.
    Проверяет, что объект сокета находится в списке авторизированных клиентов, кроме случая получения запроса на
    авторизацию.
    Если объект сокета не найден в списке авторизированных клиентов, то генерируется исключение TypeError
    :param func: Декорируемая функция
    :return: None
    """
    def decorated(*args, **kwargs):
        from server.server_core import Server
        from common.variables import ACTION, PRESENCE

        if isinstance(args[0], Server):
            is_found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            is_found = True
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        is_found = True
            if not is_found:
                raise TypeError
        return func(*args, **kwargs)
    return decorated
