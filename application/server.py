"""
Программа-сервер
"""
import json
import logging
import sys
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM

import log.server_log_config

from common.utils import get_parameters, get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MAX_CONNECTIONS, MESSAGE, \
    MESSAGE_TEXT, SENDER
from errors import IncorrectDataReceivedError
from decos import log

SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    """
    Обрабатывает сообщения от клиентов.
    Если это сообщение о присутствии - проверяет корректность и отправляет ответ клиенту.
    Если это сообщение пользователям - проверяет корректность и добавляет в очередь
    :param message: сообщение от клиента
    :param messages_list: очередь сообщений
    :param client: сокет с клиентом
    :return: None
    """

    SERVER_LOGGER.debug(f'Разбор сообщения {message} от клиента')

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad request'
        })
        raise IncorrectDataReceivedError


def main():
    """
    Главная функция сервера.
    Параметры принимаются из командной строки (-p - номер порта, -а - адрес),
    если параметров нет - принимаются параметры по умолчанию
    :return:
    """

    clients = []
    messages = []
    param = get_parameters(True)

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
    transport.settimeout(1)
    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с клиентом {client_address}')
            clients.append(client)

        recv_data_list = []
        send_data_list = []
        err_list = []

        try:
            if clients:
                recv_data_list, send_data_list, err_list = select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_list:
            for client_with_msg in recv_data_list:
                try:
                    process_client_message(get_message(client_with_msg), messages, client_with_msg)
                    SERVER_LOGGER.debug(f'Обработано сообщение клиента {client_with_msg.getpeername()}')
                except IncorrectDataReceivedError:
                    SERVER_LOGGER.info(f'Клиент {client_with_msg.getpeername()} отключился от сервера')
                    clients.remove(client_with_msg)

        if messages and send_data_list:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                    SERVER_LOGGER.debug(f'Отправлено сообщение {message} клиенту {waiting_client}')
                except IncorrectDataReceivedError:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
