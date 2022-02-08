"""
Программа-клиент
"""
import sys
import json
import logging
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

import log.client_log_config
from common.utils import get_parameters, send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MESSAGE, SENDER, \
    MESSAGE_TEXT, QUIT, RECEIVER
from errors import ReqFieldMissingError, ServerError, IncorrectDataReceivedError
from decos import log

CLIENT_LOGGER = logging.getLogger('client')


@log
def create_exit_message(account_name):
    """
    Создает словарь-сообщение о выходе
    :param account_name: Имя пользователя
    :return: Словарь
    """
    return {
        ACTION: QUIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log
def process_message_from_server(sock, my_username):
    """
    Обрабатывает сообщения других пользователей, поступающих с сервера
    :param sock: Сокет
    :param my_username: Имя теущего пользователя
    :return: None
    """
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and \
                    RECEIVER in message and MESSAGE_TEXT in message and message[RECEIVER] == my_username:
                print(f'Получено сообщение от пользователя {message[SENDER]}:\n'
                      f'{message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n'
                                   f'{message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Полочено некорректное сообщение от сервера {message}')
        except IncorrectDataReceivedError:
            CLIENT_LOGGER.error('Не удалось декодировать полученное сообщение')
        except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'Потеряно соединение {my_username} с сервером')
            break


@log
def create_presence(account_name):
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
    Функция запрашивает кому отправить сообщение м само сообщение.
    Создает сообщение для отправки другим пользователям и отправляет его на сервер.
    :param sock: сокет
    :param account_name: имя пользователя
    :return: None
    """
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')

    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        RECEIVER: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')

    try:
        send_message(sock, message_dict)
        CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
    except Exception as err:
        print(err)
        CLIENT_LOGGER.critical(f'Потеряно соединение {account_name} с сервером')
        time.sleep(3)
        sys.exit(1)


def print_help():
    """
    Выводит справку по работе с программой
    :return: None
    """
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Получатель и текст будут запрошены отдельно')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def user_interactive(sock, username):
    """
    Функция взаимодействия с пользователем. Запрашивает от пользователя команды, отправляет сообщения
    :param sock: Сокет
    :param username: Имя пользователя
    :return: None
    """
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя')
            time.sleep(2)
            break
        else:
            print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды')


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
    client_name = param.name

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта '
                               f'{server_port}. Допустимые номера порта: от 1024 до 65535. '
                               f'Клиент завершается.')
        sys.exit(1)

    if not client_name:
        client_name = input('Введите имя пользователя: ')

    CLIENT_LOGGER.info(f'Запущен клиент с параметрами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')

    message_to_server = create_presence(client_name)

    CLIENT_LOGGER.info(f'Сформировано сообщение на сервер {message_to_server}')

    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((server_address, server_port))
        send_message(client, message_to_server)
        answer = process_answ(get_message(client))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        print(f'Установлено соединение клиента {client_name} с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную JSON строку')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address} : {server_port}. '
                               f'Сервер отверг запрос на подключение.')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=process_message_from_server, args=(client, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(client, client_name))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
