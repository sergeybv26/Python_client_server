"""
Программа-клиент. Объектно-ориентированный стиль
"""
import json
import logging
import socket
import sys
import threading
import time

import log.client_log_config
from common.utils import send_message, get_message, get_parameters
from common.variables import ACTION, QUIT, TIME, ACCOUNT_NAME, MESSAGE, SENDER, RECEIVER, MESSAGE_TEXT, PRESENCE, USER, \
    RESPONSE, ERROR
from errors import IncorrectDataReceivedError, ReqFieldMissingError, ServerError
from metaclasses import ClientMaker
from decos import log

CLIENT_LOGGER = logging.getLogger('client')


class ClientSender(threading.Thread, metaclass=ClientMaker):

    # Класс формирования и отправки сообщений на сервер

    def __init__(self, account_name, sock):
        self.client_name = account_name
        self.transport = sock
        super().__init__()

    def create_exit_message(self):
        """
        Создает словарь-сообщение о выходе
        :return: Словарь
        """
        return {
            ACTION: QUIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.client_name
        }

    def create_message(self):
        """
        Функция запрашивает кому отправить сообщение м само сообщение.
        Создает сообщение для отправки другим пользователям и отправляет его на сервер.
        :return: None
        """
        receiver_name = input('Введите получателя сообщения: ')
        message = input('Введите сообщение для отправки: ')

        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.client_name,
            RECEIVER: receiver_name,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')

        try:
            send_message(self.transport, message_dict)
            CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {receiver_name}')
        except Exception as err:
            print(err)
            CLIENT_LOGGER.critical(f'Потеряно соединение {self.client_name} с сервером')
            sys.exit(1)

    @staticmethod
    def print_help():
        """
        Выводит справку по работе с программой
        :return: None
        """
        print('Поддерживаемые команды:')
        print('message - отправить сообщение. Получатель и текст будут запрошены отдельно')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')

    def run(self):
        """
        Функция взаимодействия с пользователем. Запрашивает от пользователя команды, отправляет сообщения
        :return: None
        """
        self.print_help()
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                send_message(self.transport, self.create_exit_message())
                print('Завершение соединения.')
                CLIENT_LOGGER.info('Завершение работы по команде пользователя')
                time.sleep(0.5)
                break
            else:
                print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды')


class ClientReader(threading.Thread, metaclass=ClientMaker):

    # Класс приема сообщений с сервера. Принимает сообщения и выводит их в консоль

    def __init__(self, account_name, sock):
        self.client_name = account_name
        self.transport = sock
        super().__init__()

    def run(self):
        """
        Основной цикл. Принимает сообщения, выводит их в консоль. При потере соединения завершает работу
        :return: None
        """
        while True:
            try:
                message = get_message(self.transport)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and \
                        RECEIVER in message and \
                        MESSAGE_TEXT in message and message[RECEIVER] == self.client_name:
                    print(f'Получено сообщение от пользователя {message[SENDER]}:\n'
                          f'{message[MESSAGE_TEXT]}')
                    CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n'
                                       f'{message[MESSAGE_TEXT]}')
                else:
                    CLIENT_LOGGER.error(f'Полочено некорректное сообщение от сервера {message}')
            except IncorrectDataReceivedError:
                CLIENT_LOGGER.error('Не удалось декодировать полученное сообщение')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                CLIENT_LOGGER.critical(f'Потеряно соединение {self.client_name} с сервером')
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


@log
def check_client_parameters():
    """
    Выполняет проверку параметров клиента
    :return: Кортеж - параметры клиента
    """
    params = get_parameters()
    server_address, server_port, client_name = params.a, params.p, params.name

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта '
                               f'{server_port}. Допустимые номера порта: от 1024 до 65535. '
                               f'Клиент завершается.')
        sys.exit(1)

    if not client_name:
        client_name = input('Введите имя пользователя: ')

    return server_address, server_port, client_name


def main():
    """
    Функция запуска консольного мессенджера
    :return: None
    """
    print('Консольный мессенджер. Клиентский модуль')

    server_address, server_port, client_name = check_client_parameters()

    print(f'Клиентский модуль запущен с именем пользователя: {client_name}')

    CLIENT_LOGGER.info(f'Запущен клиент с парамтрами: '
                       f'адрес сервера - {server_address}, '
                       f'порт - {server_port}, '
                       f'имя пользователя - {client_name}.')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_answ(get_message(transport))
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
        module_receiver = ClientReader(client_name, transport)
        module_receiver.daemon = True
        module_receiver.start()

        module_sender = ClientSender(client_name, transport)
        module_sender.daemon = True
        module_sender.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if module_receiver.is_alive() and module_sender.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
