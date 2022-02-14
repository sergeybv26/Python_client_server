"""
Программа-сервер. Объектно-ориентированный стиль
"""
import logging
import time
from select import select
import socket

from common.utils import get_message, send_message, get_parameters
from common.variables import MAX_CONNECTIONS, RECEIVER, SENDER, ACTION, MESSAGE, TIME, MESSAGE_TEXT, PRESENCE, USER, \
    ACCOUNT_NAME, RESPONSE, RESPONSE_400, ERROR, QUIT
from descrptrs import Port
from errors import IncorrectDataReceivedError, MissingClient
from metaclasses import ServerMaker
import log.server_log_config


class Server(metaclass=ServerMaker):
    port = Port()

    def __init__(self, listen_address, listen_port):
        self.addr = listen_address
        self.port = listen_port
        self.logger = logging.getLogger('server')
        self.clients = []
        self.messages = []
        self.names = {}
        self.sock = None

    def init_socket(self):
        self.logger.info(f'Запущен сервер. Порт для подключений: {self.port}.'
                         f'Подключения принимаются с адреса: {self.addr}. '
                         f'Если адрес не указан, соединения принимаются с любых адресов')
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)

    def main_loop(self):
        self.init_socket()

        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                self.logger.info(f'Установлено соединение с клиентом {client_address}')
                self.clients.append(client)

            recv_data_list = []
            send_data_list = []
            err_list = []

            try:
                if self.clients:
                    recv_data_list, send_data_list, err_list = select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if recv_data_list:
                for client_with_msg in recv_data_list:
                    try:
                        self.process_client_message(get_message(client_with_msg), client_with_msg)
                    except IncorrectDataReceivedError:
                        self.logger.info(f'Клиент {client_with_msg.getpeername()} отключился от сервера')
                        self.clients.remove(client_with_msg)
                    except MissingClient:
                        self.logger.error('Потеря связи с клиентом')
                        if client_with_msg in self.clients:
                            self.clients.remove(client_with_msg)
                        recv_data_list.remove(client_with_msg)
                        for key in self.names.keys():
                            if self.names[key] == client_with_msg:
                                del self.names[key]
                                break

            for msg in self.messages:
                try:
                    self.process_message(msg, send_data_list)
                except (ConnectionError, TypeError):
                    self.logger.error(f'Связь с клиентом {msg[RECEIVER]} была потеряна.')
                    self.clients.remove(self.names[msg[RECEIVER]])
                    del self.names[msg[RECEIVER]]
            self.messages.clear()

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
            self.logger.debug(f'Соединение с клиентом {message[ACCOUNT_NAME]} закрывается по инициативе клиента')
            self.names[message[ACCOUNT_NAME]].close()
            del self.names[message[ACCOUNT_NAME]]
            return
        else:
            response = RESPONSE_400
            response[ERROR] = 'Получен некорректный запрос'
            send_message(client, response)
            raise IncorrectDataReceivedError


def main():
    """
    Функция, которая получает параметры командной строки и запускает сервер
    :return: None
    """
    param = get_parameters(True)
    listen_address, listen_port = param.a, param.p

    server = Server(listen_address, listen_port)
    server.main_loop()


if __name__ == '__main__':
    main()
