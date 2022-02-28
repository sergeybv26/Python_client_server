"""
Общие функции для клиента и сервера
"""
import argparse
import json
import sys

from common import variables


sys.path.append('../')
from common.decos import log


@log
def send_message(sock, message):
    """
    Выполняет кодирование и отправку сообщения
    :param sock: сокет
    :param message: Отправляемое сообщение
    :return: None
    """
    if not isinstance(message, dict):
        raise TypeError

    js_message = json.dumps(message)
    encoded_message = js_message.encode(variables.ENCODING)
    sock.send(encoded_message)


@log
def get_message(sock):
    """
    Принимает и декодирует сообщение. Если принят не словарь - выдает ошибку
    :param sock: сокет
    :return: словарь ответа
    """

    # try:
    encoded_response = sock.recv(variables.MAX_PACKAGE_LENGTH)
    # except (ConnectionResetError, OSError):
    #     raise MissingClient

    if isinstance(encoded_response, bytes):
        js_response = encoded_response.decode(variables.ENCODING)
        response = json.loads(js_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


@log
def get_parameters(is_server=False):
    """
    Получает параметры IP адреса и порта из командной строки.
    Получает параметр клиента из командной строки
    :param is_server: Признак, указывающий, что это настройки для сервера
    :return: возвращает параметры
    """

    parser_param = argparse.ArgumentParser()
    if not is_server:
        parser_param.add_argument('-a', default=variables.DEFAULT_IP_ADDRESS)
    else:
        parser_param.add_argument('-a', default='')
    parser_param.add_argument('-p', default=variables.DEFAULT_PORT, type=int, nargs='?')
    parser_param.add_argument('-n', '--name', default=None, nargs='?')

    parameters = parser_param.parse_args(sys.argv[1:])

    return parameters
