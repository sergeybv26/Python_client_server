"""
Программа-сервер
"""
import json
import logging
import sys
from socket import socket, AF_INET, SOCK_STREAM

import log.server_log_config

from common.utils import get_tcp_parameters, get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MAX_CONNECTIONS
from errors import IncorrectDataReceivedError
from decos import log

SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message):
    """
    Обрабатывает сообщения от клиентов
    :param message: сообщение от клиента
    :return: словарь-ответ
    """

    SERVER_LOGGER.debug(f'Разбор сообщения {message} от клиента')

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad request'
    }


def main():
    """
    Главная функция сервера.
    Параметры принимаются из командной строки (-p - номер порта, -а - адрес),
    если параметров нет - принимаются параметры по умолчанию
    :return:
    """

    param = get_tcp_parameters(True)

    listen_address = param.a
    listen_port = int(param.p)

    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с неподходящим номером порта '
                               f'{listen_port}. Допустимые номера порта: от 1024 до 65535')
        sys.exit(1)

    SERVER_LOGGER.info(f'Запущен сервер. Порт для подключений: {listen_port}.'
                       f'Подключения принимаются с адреса: {listen_address}. '
                       f'Если адрес не указан, соединения принимаются с любых адресов')

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соединение с клиентом {client_address}')

        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение от клиента: {message_from_client}')
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную '
                                f'от клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataReceivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается')
            client.close()


if __name__ == '__main__':
    main()
