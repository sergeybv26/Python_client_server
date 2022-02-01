"""
Программа-клиент
"""
import sys
import json
import logging
import time
from socket import socket, AF_INET, SOCK_STREAM

import log.client_log_config
from common.utils import get_parameters, send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MESSAGE, SENDER, MESSAGE_TEXT
from errors import ReqFieldMissingError, ServerError
from decos import log

CLIENT_LOGGER = logging.getLogger('client')


@log
def parser_message(message):
    """
    Функция обрабатывает сообщения от других пользователей, поступающие от сервера
    :param message: Сообщение
    :return: None
    """
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and \
            MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n'
                           f'{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение от сервера: {message}')


@log
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


@log
def create_message(sock, account_name='Guest'):
    """
    Функция создает сообщение для отправки другим пользователям через сервер.
    Завершает работу при вводе '!!!'
    :param sock: сокет
    :param account_name: имя пользователя
    :return: Словарь - сообщение
    """
    message = input('Введите сообщение для отправки или "!!!" для завершения работы: ')

    if message == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде от пользователя')
        sys.exit(0)

    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение для отправки пользователю: {message_dict}')

    return message_dict


@log
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
    Параметры принимаются из командной строки (-p - номер порта, -а - адрес, -m - режим работы клиента),
    если параметров нет - принимаются параметры по умолчанию
    :return:
    """
    param = get_parameters()

    server_address = param.a
    server_port = int(param.p)
    client_mode = param.m

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта '
                               f'{server_port}. Допустимые номера порта: от 1024 до 65535. '
                               f'Клиент завершается.')
        sys.exit(1)

    if client_mode == 'send':
        print('Режим работы - отправка сообщений')
    elif client_mode == 'listen':
        print('Режим работы - прием сообщений')
    else:
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}. '
                               f'Допустимые режимы: listen, send')
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
        print('Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную JSON строку')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address} : {server_port}. '
                               f'Сервер отверг запрос на подключение.')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
        sys.exit(1)
    else:
        while True:
            if client_mode == 'send':
                try:
                    send_message(client, create_message(client))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
            if client_mode == 'listen':
                try:
                    parser_message(get_message(client))
                except (ConnectionError, ConnectionResetError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
