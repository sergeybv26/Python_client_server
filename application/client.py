"""
Программа-клиент. Объектно-ориентированный стиль
"""
import json
import logging
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM

from common.utils import get_parameters, get_message, send_message
from common.variables import ACTION, QUIT, TIME, ACCOUNT_NAME, SENDER, MESSAGE, RECEIVER, MESSAGE_TEXT, PRESENCE, USER
from errors import IncorrectDataReceivedError


class Client:
    def __init__(self):
        self.logger = logging.getLogger('client')
        self.param = get_parameters()
        self.server_address = self.param.a
        self.server_port = self.param.p
        self.client_name = self.param.name
        self.receiver_name = None
        self.transport = socket(AF_INET, SOCK_STREAM)
        self.message = None
        self.request = None
        self.message_dict = None
        self.command = None

    def check_client_parameters(self):
        """
        Выполняет проверку параметров клиента
        :return: None
        """
        if not 1023 < self.server_port < 65536:
            self.logger.critical(f'Попытка запуска клиента с неподходящим номером порта '
                                   f'{self.server_port}. Допустимые номера порта: от 1024 до 65535. '
                                   f'Клиент завершается.')
            sys.exit(1)

        if not self.client_name:
            self.client_name = input('Введите имя пользователя: ')

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

    def process_message_from_server(self):
        """
        Обрабатывает сообщения других пользователей, поступающих с сервера
        :return: None
        """
        while True:
            try:
                self.message = get_message(self.transport)
                if ACTION in self.message and self.message[ACTION] == MESSAGE and SENDER in self.message and \
                        RECEIVER in self.message and \
                        MESSAGE_TEXT in self.message and self.message[RECEIVER] == self.client_name:
                    print(f'Получено сообщение от пользователя {self.message[SENDER]}:\n'
                          f'{self.message[MESSAGE_TEXT]}')
                    self.logger.info(f'Получено сообщение от пользователя {self.message[SENDER]}:\n'
                                       f'{self.message[MESSAGE_TEXT]}')
                else:
                    self.logger.error(f'Полочено некорректное сообщение от сервера {self.message}')
            except IncorrectDataReceivedError:
                self.logger.error('Не удалось декодировать полученное сообщение')
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                self.logger.critical(f'Потеряно соединение {self.client_name} с сервером')
                break

    def create_presence(self):
        """
        Формирует запрос на сервер о присутствии клиента
        :return: JIM объект
        """

        self.request = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.client_name
            }
        }
        self.logger.debug(f'Сформировано сообщение {PRESENCE} для пользователя {self.client_name}')

        return self.request

    def create_message(self):
        """
        Функция запрашивает кому отправить сообщение м само сообщение.
        Создает сообщение для отправки другим пользователям и отправляет его на сервер.
        :return: None
        """
        self.receiver_name = input('Введите получателя сообщения: ')
        self.message = input('Введите сообщение для отправки: ')

        self.message_dict = {
            ACTION: MESSAGE,
            SENDER: self.client_name,
            RECEIVER: self.receiver_name,
            TIME: time.time(),
            MESSAGE_TEXT: self.message
        }
        self.logger.debug(f'Сформирован словарь сообщения: {self.message_dict}')

        try:
            send_message(self.transport, self.message_dict)
            self.logger.info(f'Отправлено сообщение для пользователя {self.receiver_name}')
        except Exception as err:
            print(err)
            self.logger.critical(f'Потеряно соединение {self.client_name} с сервером')
            time.sleep(3)
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

    def user_interactive(self):
        """
        Функция взаимодействия с пользователем. Запрашивает от пользователя команды, отправляет сообщения
        :return: None
        """
        self.print_help()
        while True:
            self.command = input('Введите команду: ')
            if self.command == 'message':
                self.create_message()
            elif self.command == 'help':
                self.print_help()
            elif self.command == 'exit':
                send_message(self.transport, self.create_exit_message())
                print('Завершение соединения.')
                self.logger.info('Завершение работы по команде пользователя')
                time.sleep(2)
                break
            else:
                print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды')
