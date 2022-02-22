"""
Формирование транспорта, отвечающего за взаимодействие с сервером
"""
import logging
import socket
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from errors import ServerError

LOGGER = logging.getLogger('client')
QNT_OF_CONNECTION_ATT = 5 # Количество попыток соединения с сервером
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


    def connection_init(self, address, port):
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.settimeout(5)
        connected = False # Флаг успешного соединения
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
