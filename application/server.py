"""
Программа-сервер
"""
import json
import logging
import sys
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

import log.server_log_config

from common.utils import get_parameters, get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MAX_CONNECTIONS, MESSAGE, \
    MESSAGE_TEXT, SENDER, RESPONSE_400, RECEIVER, QUIT
from errors import IncorrectDataReceivedError
from decos import log

SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client, clients, names):
    """
    Обрабатывает сообщения от клиентов.
    Если это сообщение о присутствии - проверяет корректность и отправляет ответ клиенту.
    Если это сообщение пользователям - проверяет корректность и добавляет в очередь
    :param message: сообщение от клиента
    :param messages_list: очередь сообщений
    :param client: сокет с клиентом
    :param clients: список клиентов сервера
    :param names: словарь, в котором ключ - имя пользователя, а значение - его сокет
    :return: None
    """

    SERVER_LOGGER.debug(f'Разбор сообщения {message} от клиента')

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, {RESPONSE: 200})
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            RECEIVER in message and SENDER in message and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    elif ACTION in message and ACCOUNT_NAME in message and message[ACTION] == QUIT and \
            message[ACCOUNT_NAME] in names.keys():
        clients.remove(names[message[ACCOUNT_NAME]])
        SERVER_LOGGER.debug(f'Соединение с клиентом {message[ACCOUNT_NAME]} закрывается по инициативе клиента')
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    else:
        response = RESPONSE_400
        response[ERROR] = 'Получен некорректный запрос'
        send_message(client, response)
        raise IncorrectDataReceivedError


@log
def process_message(message, names, listen_socks):
    """
    Выполняет отправку сообщения определенному клиенту
    :param message: Сообщение в виде словаря
    :param names: словарь, в котором ключ - имя пользователя, а значение - его сокет
    :param listen_socks: список сокетов
    :return: None
    """

    if message[RECEIVER] in names.keys() and names[message[RECEIVER]] in listen_socks:
        send_message(names[message[RECEIVER]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[RECEIVER]} от '
                           f'пользователя {message[SENDER]}.')
    elif message[RECEIVER] in names.keys() and names[message[RECEIVER]] not in listen_socks:
        raise ConnectionError
    else:
        response_error = {
            ACTION: MESSAGE,
            SENDER: 'Сервер мессенджера',
            RECEIVER: message[SENDER],
            TIME: time.time(),
            MESSAGE_TEXT: f'Пользователь {message[RECEIVER]} не зарегистрирован на сервере. '
                          f'Отправка сообщения не возможна'
        }
        send_message(names[message[SENDER]], response_error)
        SERVER_LOGGER.error(f'Пользователь {message[RECEIVER]} не зарегистрирован на сервере. '
                            f'Отправка сообщения не возможна')


def main():
    """
    Главная функция сервера.
    Параметры принимаются из командной строки (-p - номер порта, -а - адрес),
    если параметров нет - принимаются параметры по умолчанию
    :return:
    """

    clients = []
    messages = []
    names = {}
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
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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
                    process_client_message(get_message(client_with_msg), messages, client_with_msg, clients, names)
                    SERVER_LOGGER.debug(f'Обработано сообщение клиента {client_with_msg.getpeername()}')
                except IncorrectDataReceivedError:
                    SERVER_LOGGER.info(f'Клиент {client_with_msg.getpeername()} отключился от сервера')
                    clients.remove(client_with_msg)

        for msg in messages:
            try:
                process_message(msg, names, send_data_list)
            except (ConnectionError, TypeError):
                SERVER_LOGGER.error(f'Связь с клиентом {msg[RECEIVER]} была потеряна.')
                clients.remove(names[msg[RECEIVER]])
                del names[msg[RECEIVER]]
        messages.clear()


if __name__ == '__main__':
    main()
