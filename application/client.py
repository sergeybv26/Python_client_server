"""
Программа-клиент
"""
import sys
import json
import logging
import time
from socket import socket, AF_INET, SOCK_STREAM

import log.client_log_config
from common.utils import get_tcp_parameters, send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from errors import ReqFieldMissingError

CLIENT_LOGGER = logging.getLogger('client')


def create_presence(account_name='Guest'):
    """
    Формирует запрос на сервер о присутствии клиента
    :param account_name: Имя пользователя
    :return: JIM объект
    """

    request = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение {PRESENCE} для пользователя {account_name}')

    return request


def process_answ(message):
    """
    Разбирает ответ от сервера
    :param message: Сообщение ответа
    :return: код ответа и сообщение (при наличии)
    """
    CLIENT_LOGGER.debug(f'Выполняется разбор сообщения {message} от сервера')

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif ERROR in message:
            return f'400: {message[ERROR]}'
        raise ReqFieldMissingError(ERROR)
    raise ReqFieldMissingError(RESPONSE)


def main():
    """
    Главная функция клиента.
    Параметры принимаются из командной строки (-p - номер порта, -а - адрес),
    если параметров нет - принимаются параметры по умолчанию
    :return:
    """
    param = get_tcp_parameters()

    server_address = param.a
    server_port = int(param.p)

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта '
                               f'{server_port}. Допустимые номера порта: от 1024 до 65535. '
                               f'Клиент завершается.')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент с параметрами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')

    message_to_server = create_presence()

    CLIENT_LOGGER.info(f'Сформировано сообщение на сервер {message_to_server}')

    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((server_address, server_port))
        send_message(client, message_to_server)
        answer = process_answ(get_message(client))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную JSON строку')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address} : {server_port}. '
                               f'Сервер отверг запрос на подключение.')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')


if __name__ == '__main__':
    main()
