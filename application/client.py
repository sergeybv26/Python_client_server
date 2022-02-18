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
from client_db import ClientDB
from common.utils import send_message, get_message, get_parameters
from common.variables import ACTION, QUIT, TIME, ACCOUNT_NAME, MESSAGE, SENDER, RECEIVER, MESSAGE_TEXT, PRESENCE, USER, \
    RESPONSE, ERROR, GET_CONTACTS, LIST_INFO, ADD_CONTACT, USERS_REQUEST, REMOVE_CONTACT
from errors import IncorrectDataReceivedError, ReqFieldMissingError, ServerError
from metaclasses import ClientMaker
from decos import log

CLIENT_LOGGER = logging.getLogger('client')

sock_lock = threading.Lock()
database_lock = threading.Lock()


class ClientSender(threading.Thread, metaclass=ClientMaker):

    # Класс формирования и отправки сообщений на сервер

    def __init__(self, account_name, sock, database):
        self.client_name = account_name
        self.transport = sock
        self.database = database
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

        with database_lock:
            if not self.database.check_user(receiver_name):
                CLIENT_LOGGER.error(f'Попытка отправить сообщение незарегистрированному получателю: {receiver_name}')
                return

        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.client_name,
            RECEIVER: receiver_name,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')

        with database_lock:
            self.database.save_message(self.client_name, receiver_name, message)

        with sock_lock:
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
        print('history - история сообщений')
        print('contacts - список контактов')
        print('edit - редактирование списка контактов')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')

    def print_history(self):
        ask = input('Показать входящие сщщбщения - in, исходящие - out, все - Enter: ')
        with database_lock:
            if ask == 'in':
                history_list = self.database.get_history(to_user=self.client_name)
                for elem in history_list:
                    print(f'\nСообщение от пользователя: {elem[0]} от {elem[3]}:\n{elem[2]}')
            elif ask == 'out':
                history_list = self.database.get_history(from_user=self.client_name)
                for elem in history_list:
                    print(f'\nСообщение пользователю: {elem[1]} от {elem[3]}:\n{elem[2]}')
            else:
                history_list = self.database.get_history()
                for elem in history_list:
                    print(f'\nСообщение от пользователя: {elem[0]}, пользователю {elem[1]} от {elem[3]}:\n{elem[2]}')

    def edit_contacts(self):
        ask = input('Для удаления введите del, для добавления - add: ')
        if ask == 'del':
            username = input('Введите имя удаляемого контакта: ')
            with database_lock:
                if self.database.check_user(username):
                    self.database.del_contact(username)
                else:
                    CLIENT_LOGGER.error(f'Попытка удаления несуществующего контакта {username}')
        elif ask == 'add':
            username = input('Введите имя создаваемого контакта: ')
            if self.database.check_user(username):
                with database_lock:
                    self.database.add_contact(username)
                with sock_lock:
                    try:
                        add_contact(self.transport, self.client_name, username)
                    except ServerError:
                        CLIENT_LOGGER.error('Не удалось отправить информацию на сервер')

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
                with sock_lock:
                    try:
                        send_message(self.transport, self.create_exit_message())
                    except Exception as err:
                        print(err)
                    print('Завершение соединения.')
                    CLIENT_LOGGER.info('Завершение работы по команде пользователя')
                time.sleep(0.5)
                break
            elif command == 'contacts':
                with database_lock:
                    contact_list = self.database.get_contacts()
                for contact in contact_list:
                    print(contact)
            elif command == 'edit':
                self.edit_contacts()
            elif command == 'history':
                self.print_history()
            else:
                print('Команда не распознана, попробуйте снова. help - вывести поддерживаемые команды')


class ClientReader(threading.Thread, metaclass=ClientMaker):

    # Класс приема сообщений с сервера. Принимает сообщения и выводит их в консоль

    def __init__(self, account_name, sock, database):
        self.client_name = account_name
        self.transport = sock
        self.database = database
        super().__init__()

    def run(self):
        """
        Основной цикл. Принимает сообщения, выводит их в консоль. При потере соединения завершает работу
        :return: None
        """
        while True:
            time.sleep(1)
            with sock_lock:
                try:
                    message = get_message(self.transport)
                except IncorrectDataReceivedError:
                    CLIENT_LOGGER.error('Не удалось декодировать полученное сообщение')
                except OSError as err:
                    if err.errno:
                        CLIENT_LOGGER.critical(f'Потеряно соединение {self.client_name} с сервером')
                        break
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                    CLIENT_LOGGER.critical(f'Потеряно соединение {self.client_name} с сервером')
                    break
                else:
                    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and \
                            RECEIVER in message and \
                            MESSAGE_TEXT in message and message[RECEIVER] == self.client_name:
                        print(f'Получено сообщение от пользователя {message[SENDER]}:\n'
                              f'{message[MESSAGE_TEXT]}')
                        with database_lock:
                            try:
                                self.database.save_message(message[SENDER], self.client_name, message[MESSAGE_TEXT])
                            except Exception as err:
                                print(err)
                                CLIENT_LOGGER.error(f'Ошибка взаимодействия с базой данных: {err}')
                        CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n'
                                           f'{message[MESSAGE_TEXT]}')
                    else:
                        CLIENT_LOGGER.error(f'Полочено некорректное сообщение от сервера {message}')


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


def contacts_list_request(sock, name):
    """
    Функция запроса списка контактов для пользователя
    :param sock: сокет
    :param name: имя пользователя
    :return: список контактов
    """
    CLIENT_LOGGER.debug(f'Запрос списка контактов для пользователя {name}')
    request = {
        ACTION: GET_CONTACTS,
        TIME: time.time(),
        USER: name
    }
    CLIENT_LOGGER.debug(f'Сформирован запрос на сервер {request}')
    send_message(sock, request)
    ans = get_message(sock)
    CLIENT_LOGGER.debug(f'Получен ответ от сервера: {ans}')
    if RESPONSE in ans and ans[RESPONSE] == 202 and LIST_INFO in ans:
        return ans[LIST_INFO]
    raise ServerError


def add_contact(sock, username, contact):
    """
    Добавление пользователя в список контактов
    :param sock: сокет
    :param username: имя текущего пользователя
    :param contact: имя добавляемого пользователя
    :return: None
    """
    CLIENT_LOGGER.debug(f'Создание контакта {contact}')
    request = {
        ACTION: ADD_CONTACT,
        TIME: time.time(),
        USER: username,
        ACCOUNT_NAME: contact
    }
    CLIENT_LOGGER.debug(f'Сформирован запрос на сервер {request}')
    send_message(sock, request)
    ans = get_message(sock)
    CLIENT_LOGGER.debug(f'Получен ответ от сервера: {ans}')
    if RESPONSE in ans and ans[RESPONSE] == 200:
        pass
    else:
        raise ServerError('Ошибка создания контакта')
    print(f'Контакт {contact} успешно создан')


def user_list_request(sock, username):
    """
    Запрашивает список известных пользователей
    :param sock: сокет
    :param username: Имя текущего пользователя
    :return: список известных пользователей
    """
    CLIENT_LOGGER.debug(f'Запрос списка известных пользователей для {username}')
    request = {
        ACTION: USERS_REQUEST,
        TIME: time.time(),
        ACCOUNT_NAME: username
    }
    CLIENT_LOGGER.debug(f'Сформирован запрос на сервер {request}')
    send_message(sock, request)
    ans = get_message(sock)
    CLIENT_LOGGER.debug(f'Получен ответ от сервера: {ans}')
    if RESPONSE in ans and ans[RESPONSE] == 202 and LIST_INFO in ans:
        return ans[LIST_INFO]
    raise ServerError


def remove_contact(sock, username, contact):
    """
    Удаляет пользователя из списка контактов
    :param sock: сокет
    :param username: текущий пользователь
    :param contact: удаляемый контакт
    :return: None
    """
    CLIENT_LOGGER.debug(f'Удаление контакта {contact}')
    request = {
        ACTION: REMOVE_CONTACT,
        TIME: time.time(),
        USER: username,
        ACCOUNT_NAME: contact
    }
    CLIENT_LOGGER.debug(f'Сформирован запрос на сервер {request}')
    send_message(sock, request)
    ans = get_message(sock)
    CLIENT_LOGGER.debug(f'Получен ответ от сервера: {ans}')
    if RESPONSE in ans and ans[RESPONSE] == 200:
        pass
    else:
        raise ServerError('Ошибка удаления контакта')
    print(f'Контакт {contact} успешно удален')


def database_load(sock, database, username):
    """
    Инициализирует базу данных при запуске. Загружает данные в базу с сервера
    :param sock: сокет
    :param database: ссылка на класс создания базы данных
    :param username: имя пользователя
    :return: None
    """
    try:
        users_list = user_list_request(sock, username)
    except ServerError:
        CLIENT_LOGGER.error(f'Ошибка запроса списка известных пользователей для {username}')
    else:
        database.add_users(users_list)

    try:
        contact_list = contacts_list_request(sock, username)
    except ServerError:
        CLIENT_LOGGER.error(f'Ошибка запроса списка контактов для {username}')
    else:
        for contact in contact_list:
            database.add_contact(contact)


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
        transport.settimeout(1)
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
        database = ClientDB(client_name)
        database_load(transport, database, client_name)

        module_receiver = ClientReader(client_name, transport, database)
        module_receiver.daemon = True
        module_receiver.start()

        module_sender = ClientSender(client_name, transport, database)
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
