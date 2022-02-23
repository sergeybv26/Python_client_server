"""
Формирование транспорта, отвечающего за взаимодействие с сервером
"""
import json
import logging
import socket
import sys
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal
sys.path.append('../')
from common.utils import send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MESSAGE, SENDER, RECEIVER, \
    MESSAGE_TEXT, GET_CONTACTS, LIST_INFO, USERS_REQUEST, ADD_CONTACT, REMOVE_CONTACT, QUIT
from errors import ServerError
import log.client_log_config

LOGGER = logging.getLogger('client')
QNT_OF_CONNECTION_ATT = 5  # Количество попыток соединения с сервером
socket_lock = threading.Lock()


class ClientTransport(threading.Thread, QObject):
    new_message = pyqtSignal(str)
    connection_lost = pyqtSignal()

    def __init__(self, address, port, database, username):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.database = database
        self.username = username
        self.transport = None
        self.connection_init(address, port)

        try:
            self.user_list_request()
            self.contacts_list_request()
        except OSError as err:
            if err.errno:
                LOGGER.critical('Потеряно соединение с сервером')
                raise ServerError('Потеряно соединение с сервером!')
            LOGGER.error('Timeout соединения при обновлении списка пользователей')
        except json.JSONDecodeError:
            LOGGER.critical('Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
        self.running = True

    def connection_init(self, address, port):
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.settimeout(5)
        connected = False  # Флаг успешного соединения
        for i in range(QNT_OF_CONNECTION_ATT):
            LOGGER.info(f'Попытка подключения к серверу №{i + 1}')
            try:
                self.transport.connect((address, port))
            except (OSError, ConnectionRefusedError):
                LOGGER.error(f'Неудачная попытка соединения с сервером №{i + 1}')
            else:
                connected = True
                break
            time.sleep(1)

        if not connected:
            LOGGER.critical('Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        LOGGER.debug('Установлено соединение с сервером')

    def create_presence(self):
        """
        Формирует запрос на сервер о присутствии клиента
        """

        request = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.username
            }
        }
        LOGGER.debug(f'Сформировано сообщение {PRESENCE} для пользователя {self.username}')

        return request

    def process_answ(self, message):
        """
        Разбирает ответ от сервера. Формирует исключение при ошибке
        :param message: Сообщение от сервера
        :return: None
        """
        LOGGER.debug(f'Выполняется разбор сообщения {message} от сервера')

        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{message[ERROR]}')
            else:
                LOGGER.error(f'Принят неизвестный код подтверждения {message[RESPONSE]}')
        elif ACTION in message and message[ACTION] == MESSAGE and \
                SENDER in message and \
                RECEIVER in message and \
                MESSAGE_TEXT in message and \
                message[RECEIVER] == self.username:
            LOGGER.debug(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            self.database.save_message(message[SENDER], 'in', message[MESSAGE_TEXT])
            self.new_message.emit(message[SENDER])

    def contacts_list_request(self):
        """
        Функция запроса и обновления списка контактов для пользователя
        :return: None
        """
        LOGGER.debug(f'Запрос списка контактов для пользователя {self.username}')
        request = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.username
        }
        LOGGER.debug(f'Сформирован запрос на сервер {request}')
        with socket_lock:
            send_message(self.transport, request)
            ans = get_message(self.transport)
        LOGGER.debug(f'Получен ответ от сервера: {ans}')
        if RESPONSE in ans and ans[RESPONSE] == 202 and LIST_INFO in ans:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            LOGGER.error('Не удалось обновить список контактов')

    def user_list_request(self):
        """
        Запрашивает список известных пользователей и обновляет таблицу
        :return: None
        """
        LOGGER.debug(f'Запрос списка известных пользователей для {self.username}')
        request = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        LOGGER.debug(f'Сформирован запрос на сервер {request}')
        with socket_lock:
            send_message(self.transport, request)
            ans = get_message(self.transport)
        LOGGER.debug(f'Получен ответ от сервера: {ans}')
        if RESPONSE in ans and ans[RESPONSE] == 202 and LIST_INFO in ans:
            self.database.add_users(ans[LIST_INFO])
        else:
            LOGGER.error('Не удалось обновить список известных пользователей')

    def add_contact(self, contact):
        """
        Сообщает на сервер о добавлении нового контакта
        :param contact: имя добавляемого пользователя
        :return: None
        """
        LOGGER.debug(f'Создание контакта {contact}')
        request = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        LOGGER.debug(f'Сформирован запрос на сервер {request}')
        with socket_lock:
            send_message(self.transport, request)
            self.process_answ(get_message(self.transport))

    def remove_contact(self, contact):
        """
        Удаляет пользователя из списка контактов
        :param contact: удаляемый контакт
        :return: None
        """
        LOGGER.debug(f'Удаление контакта {contact}')
        request = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        LOGGER.debug(f'Сформирован запрос на сервер {request}')
        with socket_lock:
            send_message(self.transport, request)
            self.process_answ(get_message(self.transport))

    def transport_shutdown(self):
        """
        Закрывает соединение. Отправляет сообщение на сервер о выходе
        :return: None
        """
        self.running = False
        message = {
            ACTION: QUIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            try:
                send_message(self.transport, message)
            except OSError:
                LOGGER.error('Ошибка отправки сообщения о выходе')
        LOGGER.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    def send_message(self, recipient, message):
        """
        Отправляет сообщение для пользователя на сервер
        :param recipient: Пользователь-получатель сообщения
        :param message: Сообщение
        :return: None
        """
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            RECEIVER: recipient,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')

        with socket_lock:
            send_message(self.transport, message_dict)
            self.process_answ(get_message(self.transport))
            LOGGER.debug(f'Отправлено сообщение для пользователя {recipient}')

    def run(self):
        LOGGER.debug('Запущен процесс обмена сообщений с сервером')
        while self.running:
            time.sleep(1)
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_message(self.transport)
                except OSError as err:
                    if err.errno:
                        LOGGER.critical('Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError,
                        json.JSONDecodeError, TypeError):
                    LOGGER.error('Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                else:
                    LOGGER.debug(f'Принято сообщение от сервера: {message}')
                    self.process_answ(message)
                finally:
                    self.transport.settimeout(5)
