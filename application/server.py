"""
Программа-сервер. Объектно-ориентированный стиль
"""
import logging
import sys
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

import log.server_log_config
from common.utils import get_parameters, send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, RESPONSE_400, ERROR, MESSAGE, \
    RECEIVER, SENDER, MESSAGE_TEXT, QUIT, MAX_CONNECTIONS
from errors import IncorrectDataReceivedError, MissingClient


class Server:
    def __init__(self):
        self.logger = logging.getLogger('server')
        self.clients = []
        self.messages = []
        self.names = {}
        self.param = get_parameters(True)
        self.transport = socket(AF_INET, SOCK_STREAM)
        self.transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.client = None
        self.client_address = None
        self.client_with_msg = None
        self.recv_data_list = []
        self.send_data_list = []
        self.err_list = []

    def process_client_message(self, message, client):
        """
        Обрабатывает сообщения от клиентов.
        Если это сообщение о присутствии - проверяет корректность и отправляет ответ клиенту.
        Если это сообщение пользователям - проверяет корректность и добавляет в очередь
        :param message: сообщение от клиента
        :param client: сокет с клиентом
        :return: None
        """

        self.logger.debug(f'Разбор сообщения {message} от клиента')

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
                USER in message:
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                send_message(client, {RESPONSE: 200})
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        elif ACTION in message and message[ACTION] == MESSAGE and \
                RECEIVER in message and SENDER in message and \
                TIME in message and MESSAGE_TEXT in message:
            self.messages.append(message)
            return
        elif ACTION in message and ACCOUNT_NAME in message and message[ACTION] == QUIT and \
                message[ACCOUNT_NAME] in self.names.keys():
            self.clients.remove(self.names[message[ACCOUNT_NAME]])
            try:
                self.recv_data_list.remove(self.names[message[ACCOUNT_NAME]])
            except ValueError:
                pass
            try:
                self.send_data_list.remove(self.names[message[ACCOUNT_NAME]])
            except ValueError:
                pass
            self.logger.debug(f'Соединение с клиентом {message[ACCOUNT_NAME]} закрывается по инициативе клиента')
            self.names[message[ACCOUNT_NAME]].close()
            del self.names[message[ACCOUNT_NAME]]
            return
        else:
            response = RESPONSE_400
            response[ERROR] = 'Получен некорректный запрос'
            send_message(client, response)
            raise IncorrectDataReceivedError

    def process_message(self, message, listen_socks):
        """
        Выполняет отправку сообщения определенному клиенту
        :param message: Сообщение в виде словаря
        :param listen_socks: список сокетов
        :return: None
        """

        if message[RECEIVER] in self.names.keys() and self.names[message[RECEIVER]] in listen_socks:
            send_message(self.names[message[RECEIVER]], message)
            self.logger.info(f'Отправлено сообщение пользователю {message[RECEIVER]} от '
                             f'пользователя {message[SENDER]}.')
        elif message[RECEIVER] in self.names.keys() and self.names[message[RECEIVER]] not in listen_socks:
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
            send_message(self.names[message[SENDER]], response_error)
            self.logger.error(f'Пользователь {message[RECEIVER]} не зарегистрирован на сервере. '
                              f'Отправка сообщения не возможна')

    def check_server_parameters(self):
        """
        Выполняет проверку параметров сервера
        :return: tuple с параметрами сервера
        """
        if not 1023 < self.param.p < 65536:
            self.logger.critical(f'Попытка запуска сервера с неподходящим номером порта '
                                 f'{self.param.p}. Допустимые номера порта: от 1024 до 65535')
            sys.exit(1)
        return self.param.a, self.param.p

    def run(self):
        """
        Осуществляет запуск и функционирование сервера
        :return: None
        """
        self.transport.bind(self.check_server_parameters())
        self.transport.settimeout(1)
        self.transport.listen(MAX_CONNECTIONS)

        self.logger.info(f'Запущен сервер. Порт для подключений: {self.param.p}.'
                         f'Подключения принимаются с адреса: {self.param.a}. '
                         f'Если адрес не указан, соединения принимаются с любых адресов')

        while True:
            try:
                self.client, self.client_address = self.transport.accept()
            except OSError:
                pass
            else:
                self.logger.info(f'Установлено соединение с клиентом {self.client_address}')
                self.clients.append(self.client)

            try:
                if self.clients:
                    self.recv_data_list, self.send_data_list, self.err_list = select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if self.recv_data_list:
                for self.client_with_msg in self.recv_data_list:
                    try:
                        self.process_client_message(get_message(self.client_with_msg), self.client_with_msg)
                    except IncorrectDataReceivedError:
                        self.logger.info(f'Клиент {self.client_with_msg.getpeername()} отключился от сервера')
                        self.clients.remove(self.client_with_msg)
                    except MissingClient:
                        self.logger.error('Потеря связи с клиентом')
                        if self.client_with_msg in self.clients:
                            self.clients.remove(self.client_with_msg)
                        self.recv_data_list.remove(self.client_with_msg)
                        for key in self.names.keys():
                            if self.names[key] == self.client_with_msg:
                                del self.names[key]
                                break

            for msg in self.messages:
                try:
                    self.process_message(msg, self.send_data_list)
                except (ConnectionError, TypeError):
                    self.logger.error(f'Связь с клиентом {msg[RECEIVER]} была потеряна.')
                    self.clients.remove(self.names[msg[RECEIVER]])
                    del self.names[msg[RECEIVER]]
            self.messages.clear()


if __name__ == '__main__':
    srv = Server()
    srv.run()
